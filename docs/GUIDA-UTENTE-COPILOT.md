# ai-standards — Guida per chi usa GitHub Copilot

Gli standard aziendali sono disponibili come **plugin di Copilot**, installabile in VS Code, IntelliJ e Copilot CLI. Non serve clonare nulla né impostare variabili d'ambiente.

## Cosa ottieni

- Le **skill** aziendali (Spring Boot, Angular, OpenAPI, test): Copilot le carica da solo quando il lavoro le riguarda.
- L'agente **aziendale**, con le regole di lavoro, sicurezza e commit.
- L'agente **code-reviewer** e i comandi `/new-endpoint`, `/new-component`, `/review`.
- I server MCP **Azure DevOps** e **Playwright** (richiedono Node.js sul PC).
- Facoltativo: il plugin **ai-standards-oracle**, con il server MCP **SQLcl** per i database Oracle.

Sono gli stessi contenuti usati da chi lavora con Kilo Code.

## Installazione

L'indirizzo del marketplace aziendale è:

```
https://github.com/NickAlmaviva/ai-standards.git
```

Ogni client ha **il proprio elenco di plugin**: se usi più client (ad esempio CLI e VS Code), installa il plugin in ciascuno.

### VS Code

1. Apri le impostazioni in formato JSON (comando **Preferences: Open User Settings (JSON)**) e aggiungi:
   ```json
   "chat.plugins.marketplaces": [
     "https://github.com/NickAlmaviva/ai-standards.git"
   ]
   ```
2. Apri la vista Estensioni (Ctrl+Shift+X), cerca `@agentPlugins` e installa **ai-standards**.

In alternativa: comando **Chat: Install Plugin From Source** e incolla l'indirizzo del repository.

Gli agent plugin di VS Code sono in anteprima: se non vedi nulla, verifica che l'impostazione `chat.plugins.enabled` sia attiva. Se è bloccata, va abilitata dagli amministratori di Copilot dell'organizzazione.

### Copilot CLI

```powershell
copilot plugin marketplace add https://github.com/NickAlmaviva/ai-standards.git
copilot plugin install ai-standards@ai-standards-marketplace
```

### IntelliJ (e altri IDE JetBrains)

Serve una versione recente del plugin GitHub Copilot (aggiornalo da **Settings → Plugins**).

1. Apri **Settings → Tools → GitHub Copilot → Customizations**, sezione **Plugins**.
2. In **Plugin Marketplaces** clicca **+** e inserisci l'indirizzo del repository:
   ```
   https://github.com/NickAlmaviva/ai-standards.git
   ```
   Clicca **Apply**.
3. Installa **ai-standards** dall'elenco dei plugin disponibili e chiudi con **OK**. Se la chat di Copilot era aperta, chiudila e riaprila.

Se Copilot non usa le skill, verifica che siano abilitate in **Settings → Tools → GitHub Copilot → Chat**, nelle opzioni dell'agente.

### Plugin facoltativo per i database Oracle

Dallo stesso marketplace puoi installare anche **ai-standards-oracle**, solo se lavori con database Oracle. Prima:

1. installa SQLcl e aggiungi la sua cartella `bin` al PATH (da un nuovo PowerShell, `sql -version` deve rispondere);
2. salva in SQLcl le connessioni da usare: **solo database di sviluppo** e, se possibile, un utente in sola lettura.

Poi installa il plugin come hai fatto per **ai-standards** (CLI: `copilot plugin install ai-standards-oracle@ai-standards-marketplace`).

### Usare una versione precisa (facoltativo)

In tutti i client l'indirizzo del marketplace può terminare con `#` seguito da un'etichetta di versione, per esempio:

```
https://github.com/NickAlmaviva/ai-standards.git#v1.1.0
```

Senza suffisso ricevi sempre l'ultima versione rilasciata, ed è la scelta consigliata. Il suffisso serve solo se ti viene chiesto di restare su una versione specifica.

## Uso quotidiano

- **Agente aziendale**: selezionalo nel selettore degli agenti della chat.
- **Nuovo endpoint**: `/new-endpoint GET /products che restituisce ...`. Copilot propone prima la specifica OpenAPI e aspetta la tua conferma.
- **Nuovo componente**: `/new-component ...`
- **Revisione**: `/review`

### Differenze rispetto a Kilo

| | Kilo | Copilot |
|---|---|---|
| Quando valgono le skill | Solo con l'agente aziendale | Con **qualunque** agente, se il plugin è attivo |
| Come si "spegne" | Si usa un altro agente | Si disattiva il plugin |
| Divieti sui comandi | Imposti dagli standard | **Non** imposti dal plugin: valgono le conferme di Copilot |

Per disattivare temporaneamente il plugin: `copilot plugin disable ai-standards` (e `enable` per riattivarlo), oppure dalla gestione plugin di VS Code o IntelliJ.

## Regole d'uso (importanti)

1. **Non attivare l'approvazione automatica dei comandi** (auto-approve in VS Code, approvazioni automatiche o assistite in IntelliJ, `--allow-all` nella CLI) quando lavori con gli standard. Con Copilot la conferma dei comandi è l'unica protezione: il plugin non può vietare comandi come fa Kilo.
2. **Leggi i comandi prima di approvarli** e rifiuta quelli che non capisci o che fanno qualcosa che non hai chiesto.
3. **Approva i tool MCP uno alla volta**: al primo avvio l'IDE può chiederti di fidarti dei server MCP del plugin, e poi di approvare le singole chiamate. Non scegliere "consenti sempre" per le azioni che modificano Azure DevOps o il database.
4. **Se Copilot dice che un'azione è stata negata**, non cercare di aggirarla.

## Aggiornamento

- **CLI**: `copilot plugin update ai-standards`
- **VS Code**: comando **Extensions: Check for Extension Updates**
- **IntelliJ**: dalla gestione plugin nelle personalizzazioni di Copilot

## Disinstallazione

`copilot plugin uninstall ai-standards`, oppure dalla gestione plugin dell'IDE.

## Contatti

Manutentori degli standard: <inserire nome, team o canale>
