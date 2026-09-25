#!/usr/bin/env python3
"""Genera i file per Kilo e per Copilot a partire dalle sorgenti condivise.

Sorgenti (le UNICHE da modificare a mano):
  shared/agent-prompts/<nome>.md            testo dell'agente (comune)
  shared/agent-prompts/<nome>.kilo.yaml     intestazione per Kilo
  shared/agent-prompts/<nome>.copilot.yaml  intestazione per Copilot
  shared/command-prompts/...                stessa logica per i comandi
  VERSION                                   versione unica per entrambi

File generati (NON modificare a mano, vengono sovrascritti):
  agents/<nome>.md, commands/<nome>.md                              -> Kilo
  com.github.copilot/agents/<nome>.agent.md,
  com.github.copilot/commands/<nome>.md                             -> Copilot
  plugin.json, .github/plugin/marketplace.json (solo il campo version)

Uso:
  python scripts/build.py          rigenera i file
  python scripts/build.py --check  verifica che siano allineati (usato dal validatore e dalla CI)

Solo libreria standard. Nel testo condiviso, {{ARGS}} indica gli argomenti
passati al comando e viene tradotto nella sintassi di ciascuno strumento.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"

# Come ogni strumento rappresenta gli argomenti di un comando
ARG_TOKEN = {"kilo": "$ARGUMENTS", "copilot": "$ARGUMENTS"}

# (cartella sorgente, strumento) -> (cartella destinazione, suffisso file)
TARGETS = {
    ("agent-prompts", "kilo"): ("agents", ".md"),
    ("agent-prompts", "copilot"): ("com.github.copilot/agents", ".agent.md"),
    ("command-prompts", "kilo"): ("commands", ".md"),
    ("command-prompts", "copilot"): ("com.github.copilot/commands", ".md"),
}

GENERATED_NOTE = {
    # Kilo e Copilot leggono il frontmatter YAML: un commento YAML e' innocuo
    "kilo": "# FILE GENERATO da scripts/build.py: modifica shared/ e rigenera.\n",
    "copilot": "# FILE GENERATO da scripts/build.py: modifica shared/ e rigenera.\n",
}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def expected_files() -> dict:
    """Restituisce {percorso relativo: contenuto atteso} per tutti i file generati."""
    out = {}
    for (src_dir, tool), (dst_dir, suffix) in TARGETS.items():
        for body_file in sorted((SHARED / src_dir).glob("*.md")):
            name = body_file.stem
            header_file = SHARED / src_dir / f"{name}.{tool}.yaml"
            if not header_file.exists():
                # Un prompt senza intestazione per uno strumento non viene generato per quello strumento
                continue
            header = read(header_file).rstrip("\n") + "\n"
            body = read(body_file).replace("{{ARGS}}", ARG_TOKEN[tool])
            content = "---\n" + GENERATED_NOTE[tool] + header + "---\n" + body
            out[f"{dst_dir}/{name}{suffix}"] = content

    version = read(ROOT / "VERSION").strip()

    plugin = json.loads(read(ROOT / "plugin.json"))
    plugin["version"] = version
    out["plugin.json"] = json.dumps(plugin, indent=2, ensure_ascii=False) + "\n"

    mkt_path = ".github/plugin/marketplace.json"
    mkt = json.loads(read(ROOT / mkt_path))
    mkt.setdefault("metadata", {})["version"] = version
    for entry in mkt.get("plugins", []):
        if entry.get("name") == plugin["name"]:
            entry["version"] = version
    out[mkt_path] = json.dumps(mkt, indent=2, ensure_ascii=False) + "\n"
    return out


def check() -> list:
    """Elenco dei file generati mancanti o non allineati."""
    problems = []
    for rel, content in expected_files().items():
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: mancante (lancia: python scripts/build.py)")
        elif read(p) != content:
            problems.append(f"{rel}: non allineato alle sorgenti in shared/ (lancia: python scripts/build.py)")
    # File generati orfani (sorgente cancellata)
    expected = set(expected_files())
    for dst_dir, suffix in set(TARGETS.values()):
        d = ROOT / dst_dir
        if d.exists():
            for f in d.glob(f"*{suffix}"):
                rel = f.relative_to(ROOT).as_posix()
                if rel not in expected and GENERATED_NOTE["kilo"].strip() in read(f):
                    problems.append(f"{rel}: generato ma senza sorgente in shared/ (cancellalo)")
    return problems


def build():
    for rel, content in expected_files().items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        old = read(p) if p.exists() else None
        if old != content:
            # newline="\n": stessi fine riga su Windows e Linux (vedi .gitattributes)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(content)
            print(f"aggiornato  {rel}")
    print("Build completata.")


if __name__ == "__main__":
    if "--check" in sys.argv:
        issues = check()
        for i in issues:
            print(f"ERROR {i}")
        print("Allineato." if not issues else f"{len(issues)} file da rigenerare.")
        sys.exit(1 if issues else 0)
    build()
