# =============================================================================
# ~/.zshrc — managed by macsetup
#
# This file is symlinked from <repo>/dotfiles/.zshrc into $HOME. Edit the
# canonical version in the repo, not the symlink. Existing user-written
# .zshrc files are backed up to ~/.macsetup-backups/<timestamp>/ before
# the symlink is created.
# =============================================================================

# Powerlevel10k instant prompt. Must stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ------------------------------------------------------------------------------
# Oh My Zsh
# ------------------------------------------------------------------------------
export ZSH="$HOME/.oh-my-zsh"
plugins=(autoswitch_virtualenv brew git gh wd dotnet vscode poetry docker docker-compose)
source $ZSH/oh-my-zsh.sh

# ------------------------------------------------------------------------------
# Architecture-aware Homebrew
# Sets PATH/MANPATH for brew. .zprofile already runs this for login shells,
# but we re-run here so non-login interactive shells (tmux, IDE terminals)
# also have brew in PATH.
# ------------------------------------------------------------------------------
if [ "$(uname -p)" = "i386" ]; then
    eval "$(/usr/local/bin/brew shellenv)"
    alias brew="/usr/local/bin/brew"
else
    eval "$(/opt/homebrew/bin/brew shellenv)"
    alias brew="/opt/homebrew/bin/brew"
fi

# ------------------------------------------------------------------------------
# Powerlevel10k
# ------------------------------------------------------------------------------
source $(brew --prefix powerlevel10k)/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# ------------------------------------------------------------------------------
# zsh-syntax-highlighting
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# ------------------------------------------------------------------------------
# zsh-autosuggestions
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# ------------------------------------------------------------------------------
# pyenv — Python version management.
# macsetup never runs `pyenv global`; use `pyenv local <ver>` per project.
# ------------------------------------------------------------------------------
export PIP_REQUIRE_VIRTUALENV=true
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# ------------------------------------------------------------------------------
# Poetry (legacy projects only — uv is primary for new ones)
# ------------------------------------------------------------------------------
export PATH="$HOME/.local/bin:$PATH"

# ------------------------------------------------------------------------------
# Direnv
# ------------------------------------------------------------------------------
eval "$(direnv hook zsh)"
export EDITOR="code --wait"

# ------------------------------------------------------------------------------
# Aliases
# ------------------------------------------------------------------------------
alias azsh="arch -arm64 zsh"                            # zsh in ARM mode
alias izsh="arch -x86_64 zsh"                           # zsh in Rosetta mode
alias aliases="grep '^alias' ~/.zshrc | sed 's/alias //g'"
alias lss="ls -alhS"                                     # list by size
alias lsla="ls -la"                                      # list all incl hidden
alias ch="history | grep 'git commit'"
alias pih="history | grep 'pip install'"
alias poh="history | grep 'poetry add'"
alias hg="history | grep"
alias ppip="python3 -m pip"
alias show="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
alias hide="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"
alias back='cd .. && echo "" && cd -'
