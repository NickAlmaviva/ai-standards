# Checklist backend

- [ ] Nessuna logica di business nei controller
- [ ] DTO e entity separati, mapping testato
- [ ] Validazione input con Bean Validation
- [ ] Errori gestiti dal ControllerAdvice con problem+json
- [ ] Nessun dato personale nei log
- [ ] Timeout configurati sulle chiamate esterne
- [ ] Migrazione DB (Flyway/Liquibase) se lo schema cambia, mai `ddl-auto=update`
- [ ] Test unitari sul service e test di integrazione sul controller
- [ ] Spec OpenAPI aggiornata se l'API è cambiata
