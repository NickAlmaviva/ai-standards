---
name: api-contract-openapi
description: Processo aziendale contract-first per le API tra microservizi e SAE. Usala quando devi creare, modificare, versionare o deprecare un endpoint REST, un DTO pubblico o una spec OpenAPI, o quando il frontend deve consumare un nuovo endpoint del backend.
metadata:
  owner: team-platform
  version: 1.0.0
---

# Contract-first con OpenAPI

## Flusso

1. **Prima la spec**: modifica il file OpenAPI del servizio (di norma `src/main/resources/openapi/*.yaml` o `api/openapi.yaml`). Non scrivere codice finché la spec non è definita.
2. **Retrocompatibilità**: sono ammessi senza nuova versione solo cambi additivi (nuovi endpoint, nuovi campi opzionali in response). Rimozioni, rinomine, nuovi campi obbligatori in request o cambi di tipo richiedono una nuova versione (`/v2/...`).
3. **Deprecazione**: marca `deprecated: true` nella spec e aggiungi header `Deprecation`/`Sunset` nella response; comunica la data di rimozione.
4. **Genera, non scrivere a mano**: interfacce server e client TypeScript vengono generate dalla spec con il generator già configurato nel progetto.
5. **Allinea il consumer**: se il task coinvolge anche il SAE, aggiorna il client generato e i tipi prima dei componenti.

## Convenzioni

- Path in kebab-case e plurale: `/orders`, `/order-items/{id}`.
- Campi JSON in camelCase; date in ISO 8601 UTC.
- Paginazione: `page`, `size`, response con `content` e `totalElements`.
- Errori: `application/problem+json`.
- Ogni operazione ha `operationId`, `summary` ed esempi di request/response.
