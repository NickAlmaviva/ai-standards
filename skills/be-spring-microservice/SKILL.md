---
name: be-spring-microservice
description: Convenzioni aziendali per i microservizi backend Java/Spring Boot. Usala SEMPRE quando lavori in un progetto backend (presenza di pom.xml, build.gradle, src/main/java) per creare o modificare controller, service, repository, entity, DTO, mapper, configurazioni, gestione errori, logging o integrazioni con altri microservizi, anche se l'utente non nomina Spring esplicitamente.
metadata:
  owner: team-platform
  version: 1.0.0
---

# Microservizi backend (Spring Boot)

> Adatta questa skill allo stack reale (versione Java/Spring, build tool, librerie). I punti sotto sono il default aziendale.

## Struttura dei package

```
com.tuaazienda.<servizio>
├── api/            # controller REST + DTO di request/response
├── application/    # service applicativi (casi d'uso), transazioni
├── domain/         # modello di dominio, regole di business, porte
├── infrastructure/ # repository JPA, client verso altri servizi, messaging
└── config/         # configurazione Spring
```

Le dipendenze vanno sempre verso l'interno: `api` → `application` → `domain`. Il `domain` non importa nulla di Spring Web o JPA.

## Regole

1. **Controller sottili**: validano l'input (`@Valid`), chiamano un service, mappano la risposta. Nessuna logica di business.
2. **DTO separati dalle entity**: mai esporre entity JPA nelle API. Mapping con MapStruct (o il mapper già usato nel progetto).
3. **Transazioni** solo nel layer `application` (`@Transactional` sui metodi dei service, non sui controller).
4. **Errori**: eccezioni di dominio tipizzate + un unico `@RestControllerAdvice` che restituisce `application/problem+json` (RFC 9457). Mai restituire stack trace.
5. **Logging**: SLF4J, messaggi parametrizzati (`log.info("Order {} created", id)`), niente dati personali, propagare il correlation id (MDC `traceId`).
6. **Configurazione**: proprietà in `application.yml` con valori da env var; classi `@ConfigurationProperties` tipizzate invece di `@Value` sparsi.
7. **Chiamate ad altri microservizi**: tramite client dedicato in `infrastructure/client`, con timeout espliciti, retry solo su operazioni idempotenti, circuit breaker se già presente nel progetto.
8. **Contratti**: se modifichi un endpoint pubblico, segui la skill `api-contract-openapi` prima di scrivere codice.
9. **Test**: segui la skill `testing-standards`.

## Checklist prima di chiudere il task

Leggi `references/checklist.md` e verifica ogni punto.
