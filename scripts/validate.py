#!/usr/bin/env python3
"""Valida il repository ai-standards (solo libreria standard).

Controlli:
- skills/<dir>/SKILL.md esiste, frontmatter con name e description
- name == nome directory, formato [a-z0-9-], max 64 caratteri
- description <= 1024 caratteri
- nomi skill univoci
- agente aziendale: presente, mode primary, prompt entro la dimensione massima
- agents/commands: frontmatter con description
- config template: JSONC parsabile, nessun token in chiaro
- plugin Copilot: plugin.json e marketplace.json coerenti
- file generati (Kilo e Copilot) allineati alle sorgenti in shared/
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_AGENT_PROMPT_CHARS = 6000
errors, warnings = [], []


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if line and not line.startswith((" ", "\t", "#")) and ":" in line:
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_skills():
    skills_dir = ROOT / "skills"
    seen = set()
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill = d / "SKILL.md"
        rel = skill.relative_to(ROOT)
        if not skill.exists():
            errors.append(f"{d.relative_to(ROOT)}: manca SKILL.md")
            continue
        fm = frontmatter(skill)
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not name:
            errors.append(f"{rel}: campo 'name' mancante")
        elif name != d.name:
            errors.append(f"{rel}: name '{name}' diverso dalla directory '{d.name}'")
        elif not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{rel}: name non valido (minuscole, numeri, trattini, max 64)")
        if name in seen:
            errors.append(f"{rel}: name duplicato '{name}'")
        seen.add(name)
        if not desc:
            errors.append(f"{rel}: campo 'description' mancante")
        elif len(desc) > 1024:
            errors.append(f"{rel}: description oltre 1024 caratteri ({len(desc)})")
        elif len(desc) < 80:
            warnings.append(f"{rel}: description molto corta, l'agente potrebbe non attivarla")
        lines = skill.read_text(encoding="utf-8").count("\n")
        if lines > 500:
            warnings.append(f"{rel}: {lines} righe, sposta dettagli in references/")


def check_main_agent():
    f = ROOT / "agents" / "aziendale.md"
    if not f.exists():
        errors.append("agents/aziendale.md mancante: e' l'agente che contiene gli standard")
        return
    text = f.read_text(encoding="utf-8")
    if frontmatter(f).get("mode") != "primary":
        errors.append("agents/aziendale.md: deve avere 'mode: primary'")
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    # Nel blocco bash i deny devono stare in fondo (vince l'ultima regola)
    fm_text = re.match(r"^---\s*\n(.*?)\n---", text, re.S).group(1)
    bash = re.search(r"^  bash:\s*\n((?:    .*\n|\s*\n)+)", fm_text + "\n", re.M)
    if bash:
        seen_deny = False
        for line in bash.group(1).splitlines():
            m = re.match(r'\s+"?(.+?)"?\s*:\s*(allow|ask|deny)\s*$', line)
            if not m:
                continue
            if m.group(2) == "deny":
                seen_deny = True
            elif seen_deny:
                errors.append(f"agents/aziendale.md (sorgente: shared/agent-prompts/aziendale.kilo.yaml): la regola bash '{m.group(1)}' ({m.group(2)}) sta dopo un deny; i deny devono stare in fondo")
    if len(body) > MAX_AGENT_PROMPT_CHARS:
        errors.append(f"agents/aziendale.md: prompt di {len(body)} caratteri (max {MAX_AGENT_PROMPT_CHARS}); sposta i dettagli in una skill")


def check_md_with_description(folder: str):
    for f in sorted((ROOT / folder).glob("*.md")):
        if not frontmatter(f).get("description"):
            errors.append(f"{f.relative_to(ROOT)}: frontmatter 'description' mancante")


def strip_jsonc(text: str) -> str:
    out, i, in_str = [], 0, False
    while i < len(text):
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\":
                out.append(text[i + 1]); i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True; out.append(c)
        elif text.startswith("//", i):
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        elif text.startswith("/*", i):
            i = text.index("*/", i) + 2
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def check_config():
    for rel in ("config/kilo.template.jsonc", "managed/kilo.jsonc"):
        f = ROOT / rel
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        try:
            json.loads(strip_jsonc(text))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: JSONC non valido ({e})")
        if re.search(r'"(Bearer\s+)?(glpat-|ghp_|sk-)[A-Za-z0-9_-]{8,}', text):
            errors.append(f"{rel}: sembra contenere un token in chiaro")


AP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AP_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9.-]{0,62}[a-z0-9])?$")


MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_SERVER_FIELDS = {"type", "command", "args", "env", "cwd", "url", "headers"}
ALLOWED_PLACEHOLDERS = {"${PLUGIN_ROOT}", "${PLUGIN_DATA}"}


def check_plugin_manifest(rel: str) -> str:
    try:
        plugin = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"{rel}: mancante o non valido ({e})")
        return ""
    if plugin.get("$schema") != AP_SCHEMA:
        errors.append(f"{rel}: $schema deve essere quello di Agent Plugins 1.0")
    name = plugin.get("name", "")
    if not AP_NAME_RE.match(name) or "--" in name or ".." in name:
        errors.append(f"{rel}: nome '{name}' non valido per Agent Plugins 1.0")
    allowed = {"$schema", "name", "version", "description", "author", "homepage",
               "repository", "license", "keywords", "extensions"}
    extra = set(plugin) - allowed
    if extra:
        errors.append(f"{rel}: campi non ammessi in Agent Plugins 1.0: {sorted(extra)}")
    return name


def check_mcp_json(rel: str):
    """Regole di Agent Plugins 1.0: un mcp.json non valido disattiva TUTTI gli MCP del plugin."""
    try:
        mcp = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"{rel}: non valido ({e})")
        return
    if mcp.get("$schema") != MCP_SCHEMA:
        errors.append(f"{rel}: $schema di Agent Plugins 1.0 mancante o errato")
    extra = set(mcp) - {"$schema", "mcpServers"}
    if extra:
        errors.append(f"{rel}: campi di primo livello non ammessi {sorted(extra)} (es. 'inputs' e 'servers' sono di VS Code, non di Agent Plugins)")
    for name, srv in (mcp.get("mcpServers") or {}).items():
        where = f"{rel} > {name}"
        bad = set(srv) - MCP_SERVER_FIELDS
        if bad:
            errors.append(f"{where}: campi non ammessi {sorted(bad)}")
        t = srv.get("type")
        if t not in ("stdio", "streamable-http", "sse"):
            errors.append(f"{where}: 'type' obbligatorio (stdio, streamable-http o sse)")
        if t == "stdio":
            cmd = srv.get("command", "")
            if not cmd:
                errors.append(f"{where}: 'command' mancante")
            elif " " in cmd or (("/" in cmd or "\\" in cmd) and not cmd.startswith("./")):
                errors.append(f"{where}: 'command' deve essere un solo eseguibile nel PATH (es. 'sql') o un percorso che inizia con ./ (niente percorsi assoluti)")
        for value in list(srv.get("args", [])) + list((srv.get("env") or {}).values()) + [srv.get("cwd", "")]:
            for ph in re.findall(r"\$\{[^}]*\}", str(value)):
                if ph not in ALLOWED_PLACEHOLDERS:
                    errors.append(f"{where}: segnaposto {ph} non supportato (ammessi solo ${{PLUGIN_ROOT}} e ${{PLUGIN_DATA}})")
        if "TUA-ORGANIZZAZIONE" in json.dumps(srv):
            warnings.append(f"{where}: contiene ancora il segnaposto TUA-ORGANIZZAZIONE")


def check_copilot_plugin():
    name = check_plugin_manifest("plugin.json")
    if (ROOT / "mcp.json").exists():
        check_mcp_json("mcp.json")
    try:
        mkt = json.loads((ROOT / ".github/plugin/marketplace.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f".github/plugin/marketplace.json: mancante o non valido ({e})")
        return
    if not any(p.get("name") == name for p in mkt.get("plugins", [])):
        errors.append(f"marketplace.json: nessuna voce per il plugin '{name}'")
    for entry in mkt.get("plugins", []):
        src = entry.get("source")
        if not (isinstance(src, str) and src.startswith("./")) or src.rstrip("/") == ".":
            continue
        base = src[2:].rstrip("/")
        sub_name = check_plugin_manifest(f"{base}/plugin.json")
        if sub_name and sub_name != entry.get("name"):
            errors.append(f"marketplace.json: la voce '{entry.get('name')}' punta a un plugin che si chiama '{sub_name}'")
        if (ROOT / base / "mcp.json").exists():
            check_mcp_json(f"{base}/mcp.json")
    if "TUA-ORGANIZZAZIONE" in (ROOT / "config/kilo.template.jsonc").read_text(encoding="utf-8"):
        warnings.append("config/kilo.template.jsonc: contiene ancora il segnaposto TUA-ORGANIZZAZIONE")


def check_generated():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build  # noqa: E402
    errors.extend(build.check())


if __name__ == "__main__":
    check_skills()
    check_main_agent()
    check_md_with_description("agents")
    check_md_with_description("commands")
    check_config()
    check_copilot_plugin()
    check_generated()
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} errori, {len(warnings)} warning")
    sys.exit(1 if errors else 0)
