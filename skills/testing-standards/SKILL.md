---
name: testing-standards
description: Standard aziendali per scrivere e correggere test automatici backend (JUnit 5, Mockito, Testcontainers) e frontend (Jest/Karma, Testing Library, Playwright). Usala ogni volta che scrivi, modifichi o sistemi test, aumenti la coverage, o quando un task richiede di verificare una modifica con test.
metadata:
  owner: team-platform
  version: 1.0.0
---

# Standard di test

## Principi comuni

- Test in formato **Given / When / Then**, un comportamento per test.
- Nomi descrittivi: `shouldReturn404WhenOrderDoesNotExist` / `it('shows an error when the save fails')`.
- Niente logica condizionale nei test; niente dipendenza dall'ordine di esecuzione.
- Prima di dichiarare il task concluso, esegui i test toccati e riporta l'esito.
- Obiettivo coverage sul codice nuovo: 80% righe, ma prioritizza i casi di errore e i confini.

## Backend

- **Unit**: JUnit 5 + Mockito sui service; niente contesto Spring.
- **Slice**: `@WebMvcTest` per i controller, `@DataJpaTest` per i repository.
- **Integrazione**: Testcontainers per DB e broker reali, mai H2 se in produzione si usa un altro DB.
- Asserzioni con AssertJ.

## Frontend

- Unit/componenti con il runner già configurato nel SAE; interazioni tramite Testing Library (query per ruolo/label, non per classi CSS).
- Mock HTTP con `HttpTestingController` o MSW; mai chiamate reali.
- E2E con Playwright solo per i flussi critici, selettori `data-testid` o ruoli accessibili.
