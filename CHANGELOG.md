# Changelog

## [1.1.0] - supporto GitHub Copilot
### Added
- Plugin GitHub Copilot (formato Agent Plugins 1.0): `plugin.json` alla radice e marketplace in `.github/plugin/marketplace.json`, installabile da VS Code, IntelliJ e Copilot CLI.
- `shared/`: sorgente unica del testo di agenti e comandi, con intestazioni separate per Kilo e Copilot.
- `scripts/build.py`: genera i file di Kilo (`agents/`, `commands/`) e di Copilot (`com.github.copilot/`) e sincronizza la versione nei manifesti. Il validatore segnala i file non allineati.
- `docs/GUIDA-UTENTE-COPILOT.md`.
### Changed
- Modello a rami: sviluppo su `develop`, `main` contiene solo versioni rilasciate (è il ramo distribuito dal marketplace Copilot).
- `agents/` e `commands/` sono ora file generati (contenuto per Kilo invariato, salvo una riga di commento iniziale).

## [1.0.0] - primo rilascio
Chiusura del pilota su un microservizio Spring Boot (Windows, modello interno Qwen 27B).
### Added
- `docs/GUIDA-UTENTE.md`: installazione, uso, regole d'uso, aggiornamento, disattivazione, problemi frequenti.
- Regole d'uso nel README (niente accettazione automatica con l'agente aziendale).
- Validatore: verifica che nel blocco bash dell'agente aziendale i deny stiano in fondo.
### Changed
- `docs/CONTRIBUTING.md` riscritto come guida per i manutentori: lezioni del pilota sui permessi, processo di rilascio su Windows, checklist di verifica.

## [0.2.2] - pilota
### Added
- Agente `aziendale`: sezione "Rispetto delle autorizzazioni" in cima al prompt. Dopo un'azione negata l'agente deve fermarsi e non cercare strade alternative per ottenere lo stesso effetto.
- Divieti aggiuntivi per scorciatoie di cancellazione note (`::Delete(`, `shutil.rmtree`, `rmSync`, `rimraf`).

## [0.2.1] - pilota
### Fixed
- Agente `aziendale`: i divieti sui comandi distruttivi coprono anche le varianti PowerShell (`Remove-Item -Recurse`) e cmd.exe (`rmdir /s`, `rd /s`, `del /s`), e funzionano anche quando il comando è avvolto in `if`, `;` o `&&`.
- Aggiunti divieti per `git reset --hard` e `git clean -f`.

## [0.2.0] - pilota
### Changed
- Standard "opt-in": regole e permessi spostati nell'agente primario `aziendale` (agents/aziendale.md). Fuori da quell'agente Kilo si comporta come senza standard.
- Skill aziendali e tool MCP vietati a livello globale e consentiti solo agli agenti `aziendale` e `code-reviewer`.
- `/new-endpoint` e `/new-component` girano sull'agente `aziendale`.
- `be-spring-microservice`: usa il base package esistente del progetto invece di `com.tuaazienda`.
### Removed
- Cartella `rules/` (contenuto spostato nel prompt dell'agente `aziendale`).
### Fixed
- `install.ps1` scrive la config in UTF-8 senza BOM.
### Added
- `install/uninstall.ps1` per Windows.

## [0.1.0] - pilota
### Added
- Struttura iniziale: rules, skills BE/FE/API/testing, agent code-reviewer, commands, installer, CI.
