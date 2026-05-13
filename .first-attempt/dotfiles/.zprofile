# =============================================================================
# ~/.zprofile — managed by macsetup
#
# Runs for login shells (Terminal.app startup, ssh login, etc.). Anything
# that should be in PATH for the entire login session — even before .zshrc
# runs — goes here.
# =============================================================================

# ------------------------------------------------------------------------------
# Homebrew (login shell)
# ------------------------------------------------------------------------------
if [ "$(uname -m)" = "arm64" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    eval "$(/usr/local/bin/brew shellenv)"
fi

# ------------------------------------------------------------------------------
# pyenv (login shell)
# ------------------------------------------------------------------------------
export PIP_REQUIRE_VIRTUALENV=true
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
