# Sicurezza

- Non leggere, stampare o modificare file `.env`, chiavi, certificati o cartelle `secrets/`.
- Non inserire mai credenziali, token o URL interni con credenziali nel codice, nei test o nei log.
- Configurazioni sensibili solo tramite variabili d'ambiente o secret manager già in uso nel progetto.
- Valida sempre l'input esterno (request body, query param, messaggi da code) e non costruire query SQL concatenando stringhe.
- Non loggare dati personali (email, codice fiscale, IBAN, telefono): mascherali.
- Segnala esplicitamente qualunque vulnerabilità notata durante il lavoro, anche se fuori scope.
