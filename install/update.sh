#!/usr/bin/env bash
# Aggiorna ai-standards all'ultimo tag (o a --ref specifico) e rigenera la config.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/install.sh" --dir "$(dirname "$SCRIPT_DIR")" "$@"
