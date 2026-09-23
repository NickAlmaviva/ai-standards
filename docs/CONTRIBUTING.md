# Contribuire ad ai-standards

## Quando creare cosa

| Hai bisogno di... | Crea |
|---|---|
| Una regola che vale sempre, per tutti | una voce in `rules/` (breve!) |
| Conoscenza su uno stack o un task specifico | una skill in `skills/<nome>/SKILL.md` |
| Un ruolo con permessi dedicati (review, audit) | un agent in `agents/` |
| Un flusso ripetibile lanciato dall'utente | un command in `commands/` |
| Un tool esterno | un server MCP in `config/kilo.template.jsonc` |

## Scrivere una buona skill

- `name` uguale al nome della directory, minuscolo con trattini.
- La `description` è l'unica cosa che l'agente vede prima di decidere: scrivi *cosa fa* e *quando usarla*, con i segnali concreti (file presenti nel progetto, tipo di richiesta). Meglio un po' insistente che vaga.
- `SKILL.md` sotto le 500 righe; dettagli lunghi in `references/` con indicazione di quando leggerli.
- Niente comandi shell embedded (`` !`cmd` ``) salvo necessità: richiedono approvazione e non funzionano nella variante remota.

## Processo

1. Branch + merge request.
2. `python3 scripts/validate.py` deve passare (lo esegue anche la CI).
3. Prova la modifica in locale: `install/update.sh --ref <tuo-branch>`, poi `/reload` in Kilo e un prompt realistico su un microservizio e su un SAE.
4. Review del team piattaforma.
5. Al merge: aggiorna `VERSION` e `CHANGELOG.md`, crea il tag `vX.Y.Z`.

Versioning: MAJOR se rimuovi/rinomini skill o cambi permessi in senso restrittivo, MINOR per nuove skill/regole, PATCH per correzioni di testo.
