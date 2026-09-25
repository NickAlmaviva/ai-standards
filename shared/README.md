# shared/ — sorgenti comuni a Kilo e Copilot

Qui c'è il testo di agenti e comandi, scritto **una sola volta**.
`scripts/build.py` lo combina con le intestazioni di ciascuno strumento e genera:

| Sorgente | Kilo | Copilot |
|---|---|---|
| `agent-prompts/<nome>.md` + `<nome>.kilo.yaml` / `<nome>.copilot.yaml` | `agents/<nome>.md` | `com.github.copilot/agents/<nome>.agent.md` |
| `command-prompts/<nome>.md` + `<nome>.kilo.yaml` / `<nome>.copilot.yaml` | `commands/<nome>.md` | `com.github.copilot/commands/<nome>.md` |

Regole:

- Modifica **solo** i file in questa cartella, poi lancia `python scripts/build.py`.
- Il testo (`.md`) è comune: scrivilo in modo neutro rispetto allo strumento.
- Le intestazioni (`.kilo.yaml`, `.copilot.yaml`) sono specifiche: i permessi di Kilo stanno solo in `.kilo.yaml`.
- Negli argomenti dei comandi usa `{{ARGS}}`: il generatore lo traduce nella sintassi di ogni strumento.
- Se manca l'intestazione per uno strumento, quel file non viene generato per quello strumento.
- Le **skill** non passano da qui: la cartella `skills/` alla radice è già letta da entrambi.
