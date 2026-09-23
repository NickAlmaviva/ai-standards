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


if __name__ == "__main__":
    check_skills()
    check_main_agent()
    check_md_with_description("agents")
    check_md_with_description("commands")
    check_config()
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} errori, {len(warnings)} warning")
    sys.exit(1 if errors else 0)
