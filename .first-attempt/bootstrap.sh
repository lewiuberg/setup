#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 1. Ensure uv is available — install if missing.
#    uv is normally installed via Homebrew cask, but on a fresh machine that
#    may not have happened yet. The official installer drops uv into ~/.local/bin.
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Sync deps into managed venv using macOS system Python (/usr/bin/python3).
#    pyenv is the only Python installer this project recognises for the user's
#    projects, but pyenv may not exist yet — system Python always does.
uv sync --quiet --python /usr/bin/python3

# 3. Launch the TUI.
exec uv run python -m macsetup "$@"
