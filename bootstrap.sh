#!/usr/bin/env bash
# macsetup bootstrap: ensure uv is available, sync deps, launch the wizard.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv…"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

uv sync --quiet
exec uv run python -m macsetup "$@"
