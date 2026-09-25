# ai-standards — Guida per chi usa GitHub Copilot

Gli standard aziendali sono disponibili come **plugin di Copilot**, installabile in VS Code, IntelliJ e Copilot CLI. Non serve clonare nulla né impostare variabili d'ambiente.

## Cosa ottieni

- Le **skill** aziendali (Spring Boot, Angular, OpenAPI, test): Copilot le carica da solo quando il lavoro le riguarda.
- L'agente **aziendale**, con le regole di lavoro, sicurezza e commit.
- L'agente **code-reviewer** e i comandi `/new-endpoint`, `/new-component`, `/review`.

Sono gli stessi contenuti usati da chi lavora con Kilo Code.

## Installazione

L'indirizzo del marketplace aziendale è:

```
https://git.tuaazienda.it/platform/ai-standards.git
```

### Copilot CLI (consigliato: vale anche per VS Code)

```powershell
copilot plugin marketplace add https://git.tuaazienda.it/platform/ai-standards.git
copilot plugin install ai-standards@ai-standards-marketplace
```

VS Code riconosce automaticamente i plugin installati con la CLI: dopo l'installazione basta ricaricare la finestra (comando **Developer: Reload Window**).

### VS Code

1. Apri le impostazioni in formato JSON (comando **Preferences: Open User Settings (JSON)**) e aggiungi:
   ```json
   "chat.plugins.marketplaces": [
     "https://git.tuaazienda.it/platform/ai-standards.git"
   ]
   ```
2. Apri la vista Estensioni (Ctrl+Shift+X), cerca `@agentPlugins` e installa **ai-standards**.

In alternativa: comando **Chat: Install Plugin From Source** e incolla l'indirizzo del repository.

Gli agent plugin di VS Code sono in anteprima: se non vedi nulla, verifica che l'impostazione `chat.plugins.enabled` sia attiva. Se è bloccata, va abilitata dagli amministratori di Copilot dell'organizzazione.

### IntelliJ (e altri IDE JetBrains)

Serve una versione recente del plugin GitHub Copilot. Nella chat di Copilot apri le **personalizzazioni** (Customizations), sezione **Plugins**, e installa **ai-standards** aggiungendo il marketplace o direttamente dal repository sorgente con l'indirizzo qui sopra. Le voci esatte possono variare con la versione del plugin.

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

1. **Non attivare l'approvazione automatica dei comandi** (auto-approve in VS Code, approvazioni automatiche o "assisted approvals" in IntelliJ, `--allow-all` nella CLI) quando lavori con gli standard. Con Copilot la conferma dei comandi è l'unica protezione: il plugin non può vietare comandi come fa Kilo.
2. **Leggi i comandi prima di approvarli** e rifiuta quelli che non capisci o che fanno qualcosa che non hai chiesto.
3. **Se Copilot dice che un'azione è stata negata**, non cercare di aggirarla.

## Aggiornamento

- **CLI**: `copilot plugin update ai-standards`
- **VS Code**: comando **Extensions: Check for Extension Updates**
- **IntelliJ**: dalla gestione plugin nelle personalizzazioni di Copilot

## Disinstallazione

`copilot plugin uninstall ai-standards`, oppure dalla gestione plugin dell'IDE.

## Contatti

Manutentori degli standard: <inserire nome, team o canale>
