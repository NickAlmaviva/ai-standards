#!/usr/bin/env bash
# Rimuove le variabili d'ambiente e la config generata. Il clone resta (rimuovilo a mano se vuoi).
set -euo pipefail
MARK_BEGIN="# >>> ai-standards (kilo) >>>"
MARK_END="# <<< ai-standards (kilo) <<<"
for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
  [[ -f "$f" ]] && grep -qF "$MARK_BEGIN" "$f" || continue
  awk -v b="$MARK_BEGIN" -v e="$MARK_END" '$0==b{s=1;next}$0==e{s=0;next}!s{print}' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  echo "Pulito $f"
done
rm -rf "$HOME/.config/ai-standards"
if [[ "$(uname -s)" == "Darwin" ]]; then
  launchctl unsetenv KILO_CONFIG || true
  launchctl unsetenv KILO_CONFIG_DIR || true
fi
echo "Disinstallato. Riavvia VS Code."
