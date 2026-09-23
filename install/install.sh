#!/usr/bin/env bash
# Installa/aggiorna ai-standards per Kilo Code (Linux/macOS).
# Uso: install.sh [--ref <tag|branch>] [--dir <path>] [--repo <git-url>]
set -euo pipefail

REPO_URL="${AI_STD_REPO_URL:-https://github.com/NickAlmaviva/ai-standards.git}"
INSTALL_DIR="${AI_STD_HOME:-$HOME/.ai-standards}"
REF=""
GEN_DIR="$HOME/.config/ai-standards"
GEN_FILE="$GEN_DIR/kilo.jsonc"
MARK_BEGIN="# >>> ai-standards (kilo) >>>"
MARK_END="# <<< ai-standards (kilo) <<<"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref)  REF="$2"; shift 2 ;;
    --dir)  INSTALL_DIR="$2"; shift 2 ;;
    --repo) REPO_URL="$2"; shift 2 ;;
    -h|--help) sed -n '2,3p' "$0"; exit 0 ;;
    *) echo "Argomento sconosciuto: $1" >&2; exit 1 ;;
  esac
done

log() { printf '\033[1;34m[ai-standards]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[ai-standards]\033[0m %s\n' "$*" >&2; }

command -v git >/dev/null || { echo "git non trovato" >&2; exit 1; }

# 1. Clone o fetch
if [[ -d "$INSTALL_DIR/.git" ]]; then
  log "Aggiorno $INSTALL_DIR"
  git -C "$INSTALL_DIR" fetch --tags --prune --quiet origin
else
  log "Clono $REPO_URL in $INSTALL_DIR"
  git clone --quiet "$REPO_URL" "$INSTALL_DIR"
fi

# 2. Checkout della versione (default: ultimo tag semver, altrimenti main)
if [[ -z "$REF" ]]; then
  REF="$(git -C "$INSTALL_DIR" tag --list 'v*' --sort=-v:refname | head -n1 || true)"
  [[ -z "$REF" ]] && REF="main"
fi
log "Versione: $REF"
git -C "$INSTALL_DIR" -c advice.detachedHead=false checkout --quiet "$REF"
if git -C "$INSTALL_DIR" show-ref --verify --quiet "refs/remotes/origin/$REF"; then
  git -C "$INSTALL_DIR" merge --ff-only --quiet "origin/$REF"
fi

# 3. Genera la config con path assoluti
ABS_DIR="$(cd "$INSTALL_DIR" && pwd)"
mkdir -p "$GEN_DIR"
ESCAPED="$(printf '%s' "$ABS_DIR" | sed 's/[&|\\]/\\&/g')"
sed "s|__AI_STANDARDS_HOME__|$ESCAPED|g" "$ABS_DIR/config/kilo.template.jsonc" > "$GEN_FILE.tmp"
mv "$GEN_FILE.tmp" "$GEN_FILE"
echo "$REF" > "$GEN_DIR/installed-ref"
log "Config generata: $GEN_FILE"

# 4. Variabili d'ambiente nei profili shell (blocco idempotente)
ENV_BLOCK="$MARK_BEGIN
export KILO_CONFIG=\"$GEN_FILE\"
export KILO_CONFIG_DIR=\"$ABS_DIR\"
$MARK_END"

write_block() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  if grep -qF "$MARK_BEGIN" "$file"; then
    # rimuove il blocco precedente
    awk -v b="$MARK_BEGIN" -v e="$MARK_END" '
      $0==b {skip=1; next} $0==e {skip=0; next} !skip {print}' "$file" > "$file.ai-std.tmp"
    mv "$file.ai-std.tmp" "$file"
  fi
  printf '\n%s\n' "$ENV_BLOCK" >> "$file"
  log "Variabili scritte in $file"
}

touched=0
for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
  if [[ -f "$f" ]]; then write_block "$f"; touched=1; fi
done
if [[ $touched -eq 0 ]]; then
  touch "$HOME/.profile"; write_block "$HOME/.profile"
fi

# 5. macOS: rende le variabili visibili anche alle app avviate dal Dock
if [[ "$(uname -s)" == "Darwin" ]]; then
  launchctl setenv KILO_CONFIG "$GEN_FILE" || true
  launchctl setenv KILO_CONFIG_DIR "$ABS_DIR" || true
  log "launchctl setenv eseguito (valido fino al riavvio; al login i profili shell vengono riletti da VS Code)"
fi

# 6. Controlli finali
for v in AI_STD_GITLAB_TOKEN; do
  if [[ -z "${!v:-}" ]]; then
    warn "Variabile $v non impostata: il relativo server MCP non si autenticherà."
  fi
done
if [[ -f "$HOME/.config/kilo/kilo.jsonc" || -f "$HOME/.config/kilo/kilo.json" ]]; then
  warn "Esiste una config globale personale in ~/.config/kilo: le chiavi in conflitto verranno sovrascritte da ai-standards (caricato dopo)."
fi

log "Fatto. Chiudi completamente VS Code e riaprilo, poi verifica con 'kilo config check'."
