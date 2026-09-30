# ai-standards — Guida per chi usa Kilo

> Usi GitHub Copilot (VS Code, IntelliJ o CLI)? Segui invece [GUIDA-UTENTE-COPILOT.md](GUIDA-UTENTE-COPILOT.md).

Questa guida ti permette di lavorare con Kilo Code secondo gli standard aziendali. Richiede circa 10 minuti, una volta sola.

## Cosa ottieni

In Kilo compare un agente chiamato **aziendale**. Quando lo selezioni, Kilo:

- segue le regole aziendali (modo di lavorare, sicurezza, commit);
- conosce le convenzioni dei nostri stack (Spring per il backend, Angular per i SAE, OpenAPI, test) e le applica da solo quando servono;
- ti mette a disposizione i comandi `/new-endpoint`, `/new-component` e `/review`;
- rispetta dei permessi: alcuni comandi partono da soli, altri chiedono conferma, quelli pericolosi sono vietati.

Con gli altri agenti (Code, Plan, Debug...) Kilo funziona esattamente come prima. **Nessun repository di progetto viene modificato.**

## Prerequisiti

- Windows con PowerShell
- Git installato e accesso al repository `ai-standards`
- VS Code con l'estensione Kilo Code aggiornata all'ultima versione
- Node.js (serve per avviare i server MCP di Azure DevOps e Playwright)
- Solo se lavori con database Oracle: SQLcl, con la sua cartella `bin` nel PATH (vedi più sotto)

## Installazione

### 1. Scarica gli standard

Apri PowerShell e lancia:

```powershell
git clone https://github.com/NickAlmaviva/ai-standards.git "$HOME\.ai-standards"
```

Se Git chiede di accedere, usa le tue credenziali aziendali.

### 2. Attivali

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\.ai-standards\install\install.ps1"
```

Lo script si posiziona sull'ultima versione rilasciata e dice a Kilo dove trovare gli standard. `-ExecutionPolicy Bypass` vale solo per questa esecuzione e non modifica le impostazioni del PC.

Alla fine devi leggere `Fatto.`. Gli avvisi gialli su token MCP o su una configurazione personale esistente sono normali.

### 3. Riavvia VS Code

Chiudi **tutte** le finestre di VS Code. In Gestione attività (Ctrl+Shift+Esc) verifica che non siano rimasti processi *Visual Studio Code* o *kilo*; se ci sono, terminali. Poi riapri VS Code.

### 4. Verifica

Nel selettore degli agenti di Kilo deve comparire **aziendale**. Selezionalo, apri una nuova sessione su un progetto e chiedi:

> Quali skill e regole aziendali hai a disposizione?

La risposta deve citare le skill `be-spring-microservice`, `fe-angular-sae`, `api-contract-openapi` e `testing-standards`.

## Uso quotidiano

- **Per usare gli standard**: seleziona l'agente **aziendale** all'inizio della sessione.
- **Nuovo endpoint**: `/new-endpoint GET /products che restituisce ...`. Kilo propone prima la specifica OpenAPI e aspetta la tua conferma.
- **Nuovo componente**: `/new-component ...`
- **Revisione delle modifiche**: `/review`. La revisione non modifica nessun file.

### Far partire un progetto direttamente con l'agente aziendale (facoltativo)

Dalla cartella del progetto:

```powershell
New-Item -ItemType Directory -Force .kilo | Out-Null
'{ "default_agent": "aziendale" }' | Set-Content -Encoding ascii .kilo\kilo.jsonc
Add-Content .git\info\exclude ".kilo/"
```

L'ultima riga fa sì che Git ignori la cartella `.kilo` solo sul tuo PC: il repository del progetto non cambia.

## Server MCP (strumenti esterni)

Con l'agente aziendale Kilo può usare:

- **Azure DevOps**: work item, repository, pipeline, wiki. Alla prima chiamata si apre il browser per l'accesso con il tuo account aziendale.
- **Playwright**: apre un browser per provare le applicazioni web.
- **SQLcl** (database Oracle): **spento di default**, si accende per singolo progetto.

Kilo legge liberamente da Azure DevOps, ma chiede conferma prima di ogni modifica, e prima di ogni azione su Playwright e sul database.

### Attivare SQLcl su un progetto

1. Installa SQLcl e aggiungi la sua cartella `bin` al PATH (es. `C:\Program Files\Oracle\sqlcl\bin`). Da un nuovo PowerShell, `sql -version` deve rispondere.
2. Salva in SQLcl le connessioni che Kilo potrà usare. Usa **solo database di sviluppo** e, se possibile, un utente in sola lettura.
3. Nella cartella del progetto crea o modifica `.kilo\kilo.jsonc`:
   ```jsonc
   { "mcp": { "sqlcl": { "enabled": true } } }
   ```
   Se il file contiene già `default_agent`, unisci le due voci:
   ```jsonc
   { "default_agent": "aziendale", "mcp": { "sqlcl": { "enabled": true } } }
   ```
4. Se il file non deve finire nel repository, aggiungi `.kilo/` a `.git\info\exclude`.

## Regole d'uso (importanti)

1. **Con l'agente aziendale non attivare l'accettazione automatica.** La conferma dei comandi è l'ultima protezione: i divieti automatici coprono i casi più comuni, ma un modello può sempre trovare un modo diverso di scrivere un comando.
2. **Leggi i comandi prima di approvarli.** Se un comando ti sembra strano, o fa qualcosa che non hai chiesto, premi **Rifiuta**: il rifiuto ferma l'agente.
3. **Database e Azure DevOps sono sistemi reali**: leggi con attenzione ogni richiesta di conferma che riguarda una query di modifica o un cambiamento su Azure DevOps.
4. **Se Kilo ti dice che un'azione è bloccata dalle autorizzazioni**, non cercare di aggirare il blocco. Se l'azione è davvero necessaria, eseguila tu; se pensi che il blocco sia sbagliato, segnalalo ai manutentori.
5. **Non modificare i file dentro `%USERPROFILE%\.ai-standards`**: verrebbero sovrascritti, o bloccherebbero l'aggiornamento. Le proposte si inviano ai manutentori.

## Aggiornamento

Quando viene annunciata una nuova versione:

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\.ai-standards\install\install.ps1"
```

Poi riavvia VS Code come al punto 3 dell'installazione. Per verificare la versione installata:

```powershell
Get-Content "$HOME\.config\ai-standards\installed-ref"
```

Per tornare a una versione precedente, aggiungi `-Ref` con il numero di versione, ad esempio `-Ref v1.0.0`.

## Disattivazione

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\.ai-standards\install\uninstall.ps1"
```

Poi riavvia VS Code. Per riattivare, ripeti il passo 2 dell'installazione.

## Problemi frequenti

| Problema | Soluzione |
|---|---|
| L'agente *aziendale* non compare | VS Code non è stato riavviato del tutto: ripeti il punto 3. Se non basta, esci dalla sessione di Windows e rientra |
| Lo script dice `Versione: main` | Contatta i manutentori: manca l'etichetta di versione sul repository |
| Errore sui criteri di gruppo o sugli script bloccati | La policy IT impedisce gli script PowerShell: contatta i manutentori |
| Una skill non viene usata | Verifica di essere sull'agente *aziendale*; puoi anche chiederla esplicitamente ("usa la skill be-spring-microservice") |

## Contatti

Manutentori degli standard: <inserire nome, team o canale>
