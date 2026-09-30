# ai-standards

Repository centrale degli standard AI, per **Kilo Code** e **GitHub Copilot** (VS Code, IntelliJ, CLI): **agente aziendale** (regole e permessi), **skills**, **comandi** e **MCP**.

- Utenti Kilo: [docs/GUIDA-UTENTE.md](docs/GUIDA-UTENTE.md)
- Utenti Copilot: [docs/GUIDA-UTENTE-COPILOT.md](docs/GUIDA-UTENTE-COPILOT.md)
- Manutentori: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) e [shared/README.md](shared/README.md)

Le skill (`skills/`) e il testo di agenti e comandi (`shared/`) sono **comuni** ai due strumenti. Per Copilot la radice del repo è anche la radice del plugin (formato Agent Plugins 1.0) e `.github/plugin/marketplace.json` è il marketplace aziendale.
Obiettivo: tutti i microservizi (BE) e i SAE (FE) lavorano con la stessa modalità, **senza** file di configurazione AI duplicati nei singoli repository.

## Come funziona

Nessun file viene aggiunto ai repository di progetto. La configurazione arriva sulle macchine dei dev tramite due variabili d'ambiente lette da Kilo:

| Variabile | Punta a | Cosa carica |
|---|---|---|
| `KILO_CONFIG` | `~/.config/ai-standards/kilo.jsonc` (generato dall'install) | MCP e permessi globali (skill aziendali vietate fuori dall'agente Aziendale) |
| `KILO_CONFIG_DIR` | la root di questo repo clonato | `skills/`, `agents/` (incluso l'agente Aziendale), `commands/` |

## Attivazione: l'agente Aziendale (opt-in)

Gli standard sono attivi **solo quando si usa l'agente `aziendale`**. Con gli agenti integrati (Code, Plan, Debug...) Kilo si comporta come senza standard.

- **Per sessione**: seleziona "aziendale" nel selettore degli agenti di Kilo.
- **Default per un progetto, solo per te**: crea `.kilo/kilo.jsonc` con `{ "default_agent": "aziendale" }` e aggiungi `.kilo/` a `.git/info/exclude`.
- **Default per un progetto, per tutto il team**: stesso file, ma committato nel repository.
- `/new-endpoint` e `/new-component` attivano l'agente Aziendale automaticamente; `/review` usa il subagente `code-reviewer`.

Lo script di install copia `config/kilo.template.jsonc` in `~/.config/ai-standards/kilo.jsonc` (sostituendo l'eventuale placeholder `__AI_STANDARDS_HOME__` con il path del clone). Il file generato **non** sta nella root del repo, così non viene caricato due volte tramite `KILO_CONFIG_DIR`.

Poiché la config arriva via `KILO_CONFIG`, è considerata *trusted*: i riferimenti `{env:VAR}` (token MCP) vengono risolti. In un `kilo.jsonc` committato in un progetto non lo sarebbero.

## Struttura

```
ai-standards/
├── shared/                      # SORGENTI comuni di agenti e comandi (vedi shared/README.md)
├── plugin.json                  # Copilot: manifesto del plugin (Agent Plugins 1.0)
├── mcp.json                     # Copilot: server MCP del plugin principale (Azure DevOps, Playwright)
├── copilot-plugins/oracle-sqlcl/ # Copilot: plugin facoltativo con il server MCP SQLcl
├── .github/plugin/marketplace.json  # Copilot: marketplace aziendale
├── com.github.copilot/          # Copilot: agenti e comandi (GENERATI da shared/)
├── config/kilo.template.jsonc   # Kilo: MCP e permessi globali (template)
├── skills/                      # conoscenza specifica, caricata on-demand
│   ├── be-spring-microservice/
│   ├── fe-angular-sae/
│   ├── api-contract-openapi/
│   └── testing-standards/
├── agents/                      # Kilo: aziendale e code-reviewer (GENERATI da shared/)
├── commands/                    # Kilo: /review, /new-endpoint, ... (GENERATI da shared/)
├── install/                     # install/uninstall per Windows (.ps1) e Linux/macOS (.sh)
├── scripts/                     # build.py (generazione), validate.py, build_skills_index.py
├── templates/AGENTS.md.template # l'UNICO file opzionale ammesso nei progetti
├── managed/                     # esempio per enforcement via MDM
├── ci/                          # pipeline GitLab / GitHub
└── docs/                        # GUIDA-UTENTE.md (utenti) e CONTRIBUTING.md (manutentori)
```

## Installazione

**Utenti Windows: segui [docs/GUIDA-UTENTE.md](docs/GUIDA-UTENTE.md).** Manutentori: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

Riepilogo:

Linux / macOS:
```bash
curl -fsSL https://git.tuaazienda.it/platform/ai-standards/-/raw/main/install/install.sh | bash
# oppure, con clone già fatto:
./install/install.sh                # ultimo tag
./install/install.sh --ref v1.2.0   # versione specifica
```

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy Bypass -File .\install\install.ps1
powershell -ExecutionPolicy Bypass -File .\install\install.ps1 -Ref v1.2.0
```
Su Windows lo stesso comando serve anche per aggiornare. Per disattivare: `install\uninstall.ps1`.

Poi **chiudi completamente VS Code e riaprilo** (le variabili d'ambiente vengono lette all'avvio). In una nuova sessione Kilo verifica con:

- `kilo config check`
- chiedendo all'agente: *"Quali skill hai disponibili?"*

## Regole d'uso

- Con l'agente aziendale **non attivare l'accettazione automatica**: la conferma umana è l'ultima protezione.
- Leggi i comandi prima di approvarli; se sono strani, **Rifiuta** (il rifiuto ferma l'agente).
- Un'azione bloccata dalle autorizzazioni non va aggirata.

## Aggiornamento

```bash
~/.ai-standards/install/update.sh        # passa all'ultimo tag e rigenera la config
```
Poi in Kilo `/reload` o nuova sessione.

## Agente vs skill: dove mettere cosa

- **shared/agent-prompts/aziendale.md** → regole trasversali (modo di lavorare, sicurezza, git); i permessi Kilo stanno in `aziendale.kilo.yaml`. Il prompt è sempre in contesto quando l'agente è attivo: tienilo corto.
- **skills/** → tutto ciò che è specifico di uno stack o di un task. L'agente vede solo nome e descrizione e carica il contenuto quando serve. Così la skill BE viene usata sui microservizi e quella FE sui SAE, senza configurare i progetti.
- **AGENTS.md nel progetto** → solo contesto di dominio unico di quel servizio. Mai duplicare le regole centrali. Vedi `templates/AGENTS.md.template`.

## Override locali

Un progetto può disattivare un MCP ereditato o restringere permessi con un `.kilo/kilo.jsonc` minimale, ad esempio:
```jsonc
{ "mcp": { "sqlcl": { "enabled": true } } }
```
Da usare solo come eccezione motivata.

## Varianti di distribuzione

1. **Clone + env var** (default, questo repo). Supporta anche skill con comandi shell embedded.
2. **Remote URL**: la CI pubblica `skills/` + `index.json` su un host statico interno e nel config si usa `skills.urls`. Nessun clone per le skill, ma le skill remote non eseguono comandi shell e agenti/comandi vanno comunque distribuiti a parte.
3. **Managed (MDM)**: `managed/kilo.jsonc` distribuito in `/etc/kilo/`, `/Library/Application Support/kilo/` o `%ProgramData%\kilo\`. Priorità massima, non sovrascrivibile.

## Versioning

Semantic versioning con tag git (`vMAJOR.MINOR.PATCH`). Ogni rilascio aggiorna `CHANGELOG.md`. Le modifiche passano da merge request con review del team piattaforma e validazione CI (`scripts/validate.py`).
