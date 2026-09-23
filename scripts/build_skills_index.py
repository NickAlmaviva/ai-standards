#!/usr/bin/env python3
"""Costruisce dist/ per la distribuzione remota (variante skills.urls).

Output:
  dist/skills/index.json
  dist/skills/<name>/...     (tutti i file della skill)
  dist/rules/*.md            (se presenti, utilizzabili come URL in "instructions")

La 'version' di ogni skill è un hash del suo contenuto: cambia solo se la
skill cambia, così Kilo riscarica solo ciò che è stato modificato.
"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    out_skills = DIST / "skills"
    out_skills.mkdir(parents=True)
    index = {"skills": []}
    for d in sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists()):
        files = sorted(str(f.relative_to(d)).replace("\\", "/") for f in d.rglob("*") if f.is_file())
        h = hashlib.sha256()
        for rel in files:
            h.update(rel.encode()); h.update((d / rel).read_bytes())
        shutil.copytree(d, out_skills / d.name)
        index["skills"].append({"name": d.name, "version": h.hexdigest()[:12], "files": files})
    (out_skills / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    if (ROOT / "rules").exists():
        shutil.copytree(ROOT / "rules", DIST / "rules")
    print(f"dist/ generato con {len(index['skills'])} skill")


if __name__ == "__main__":
    main()
