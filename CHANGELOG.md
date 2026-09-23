# Changelog

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
