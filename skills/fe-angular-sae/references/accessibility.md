# Accessibilità — minimi obbligatori

- Ogni input ha una `<label>` associata o `aria-label`.
- Pulsanti come `<button>`, link come `<a>`: mai `div` cliccabili.
- Immagini informative con `alt`, decorative con `alt=""`.
- I dialog intrappolano il focus e lo restituiscono all'elemento di origine alla chiusura.
- Messaggi di errore dei form collegati con `aria-describedby`.
- Navigazione completa da tastiera, focus visibile.
- Contrasto testo minimo 4.5:1 (WCAG 2.1 AA).
