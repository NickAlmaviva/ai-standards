---
name: fe-angular-sae
description: Convenzioni aziendali per i SAE frontend Angular. Usala SEMPRE quando lavori in un progetto frontend (presenza di angular.json, package.json con @angular/core, src/app) per creare o modificare componenti, servizi, routing, form, state management, chiamate HTTP, stili o test frontend, anche se l'utente non nomina Angular esplicitamente.
metadata:
  owner: team-platform
  version: 1.0.0
---

# SAE frontend (Angular)

> Adatta questa skill allo stack reale (versione Angular, libreria UI, state management). I punti sotto sono il default aziendale.

## Struttura

```
src/app/
├── core/        # servizi singleton, interceptor, guard
├── shared/      # componenti, pipe, direttive riusabili (senza logica di dominio)
├── features/<feature>/
│   ├── components/
│   ├── pages/
│   ├── data-access/   # servizi HTTP, store/signal della feature
│   └── <feature>.routes.ts
└── app.config.ts
```

## Regole

1. **Standalone components** e lazy loading per feature via `loadComponent`/`loadChildren`.
2. **Change detection `OnPush`** su tutti i componenti; stato con signals (o lo store già in uso nel SAE).
3. **Componenti presentazionali vs smart**: i presentazionali ricevono `input()` ed emettono `output()`, non iniettano servizi HTTP.
4. **HTTP** solo nei servizi `data-access`, tipizzati con le interfacce generate dalla spec OpenAPI quando disponibili. Nessuna URL hardcoded: usa la configurazione d'ambiente.
5. **Gestione errori** centralizzata con un interceptor; i componenti mostrano stati di loading/errore/empty espliciti.
6. **Form**: Reactive Forms tipizzati, validazioni lato client allineate a quelle del backend.
7. **Accessibilità**: elementi semantici, label sui campi, focus gestito nei dialog, contrasto adeguato. Leggi `references/accessibility.md` quando crei componenti UI.
8. **Stili**: usa i token del design system aziendale, niente colori o spaziature hardcoded.
9. **Integrazione nel contenitore**: non modificare shell, routing globale o dipendenze condivise del SAE contenitore senza richiesta esplicita.
10. **Test**: segui la skill `testing-standards`.
