# ai-standards

Repository centrale delle regole AI per Kilo Code: **rules**, **skills**, **agents**, **commands** e **MCP**.
Obiettivo: tutti i microservizi (BE) e i SAE (FE) lavorano con la stessa modalità, **senza** file di configurazione AI duplicati nei singoli repository.

## Come funziona

Nessun file viene aggiunto ai repository di progetto. La configurazione arriva sulle macchine dei dev tramite due variabili d'ambiente lette da Kilo:

| Variabile | Punta a | Cosa carica |
|---|---|---|
| `KILO_CONFIG` | `~/.config/ai-standards/kilo.jsonc` (generato dall'install) | instructions (rules), MCP, permessi |
| `KILO_CONFIG_DIR` | la root di questo repo clonato | `skills/`, `agents/`, `commands/` |

Il file `config/kilo.template.jsonc` contiene il placeholder `__AI_STANDARDS_HOME__`; lo script di install lo sostituisce con il path assoluto del clone e scrive il risultato in `~/.config/ai-standards/kilo.jsonc`. Il file generato **non** sta nella root del repo, così non viene caricato due volte tramite `KILO_CONFIG_DIR`.

Poiché la config arriva via `KILO_CONFIG`, è considerata *trusted*: i riferimenti `{env:VAR}` (token MCP) vengono risolti. In un `kilo.jsonc` committato in un progetto non lo sarebbero.

## Struttura

```
ai-standards/
├── config/kilo.template.jsonc   # instructions, MCP, permessi (template)
├── rules/                       # sempre attive: brevi e trasversali
├── skills/                      # conoscenza specifica, caricata on-demand
│   ├── be-spring-microservice/
│   ├── fe-angular-sae/
│   ├── api-contract-openapi/
│   └── testing-standards/
├── agents/                      # subagent (es. code-reviewer)
├── commands/                    # slash command (/review, /new-endpoint, ...)
├── install/                     # install.sh, install.ps1, update.sh
├── scripts/                     # validazione + build index.json per skills.urls
├── templates/AGENTS.md.template # l'UNICO file opzionale ammesso nei progetti
├── managed/                     # esempio per enforcement via MDM
├── ci/                          # pipeline GitLab / GitHub
└── docs/                        # linee guida per contribuire
```

## Installazione (dev)

Linux / macOS:
```bash
curl -fsSL https://git.tuaazienda.it/platform/ai-standards/-/raw/main/install/install.sh | bash
# oppure, con clone già fatto:
./install/install.sh                # ultimo tag
./install/install.sh --ref v1.2.0   # versione specifica
```

Windows (PowerShell):
```powershell
.\install\install.ps1
.\install\install.ps1 -Ref v1.2.0
```

Poi **chiudi completamente VS Code e riaprilo** (le variabili d'ambiente vengono lette all'avvio). In una nuova sessione Kilo verifica con:

- `kilo config check`
- chiedendo all'agente: *"Quali skill hai disponibili?"*

## Aggiornamento

```bash
~/.ai-standards/install/update.sh        # passa all'ultimo tag e rigenera la config
```
Poi in Kilo `/reload` o nuova sessione.

## Regole vs skill: dove mettere cosa

- **rules/** → solo ciò che vale *sempre* e *ovunque* (tono, sicurezza, git). Vengono iniettate in ogni sessione: tienile corte.
- **skills/** → tutto ciò che è specifico di uno stack o di un task. L'agente vede solo nome e descrizione e carica il contenuto quando serve. Così la skill BE viene usata sui microservizi e quella FE sui SAE, senza configurare i progetti.
- **AGENTS.md nel progetto** → solo contesto di dominio unico di quel servizio. Mai duplicare le regole centrali. Vedi `templates/AGENTS.md.template`.

## Override locali

Un progetto può disattivare un MCP ereditato o restringere permessi con un `.kilo/kilo.jsonc` minimale, ad esempio:
```jsonc
{ "mcp": { "jira": { "enabled": false } } }
```
Da usare solo come eccezione motivata.

## Varianti di distribuzione

1. **Clone + env var** (default, questo repo). Supporta anche skill con comandi shell embedded.
2. **Remote URL**: la CI pubblica `skills/` + `index.json` e `rules/` su un host statico interno; nel config si usano `skills.urls` e URL in `instructions`. Nessun clone, ma le skill remote non eseguono comandi shell.
3. **Managed (MDM)**: `managed/kilo.jsonc` distribuito in `/etc/kilo/`, `/Library/Application Support/kilo/` o `%ProgramData%\kilo\`. Priorità massima, non sovrascrivibile.

## Versioning

Semantic versioning con tag git (`vMAJOR.MINOR.PATCH`). Ogni rilascio aggiorna `CHANGELOG.md`. Le modifiche passano da merge request con review del team piattaforma e validazione CI (`scripts/validate.py`).
