#!/usr/bin/env zsh

source functions.sh
source constants.sh

#h! Terminal ##################################################################
frame_text "Terminal"

#h! Terminal: Oh My Zsh #######################################################
frame_text "Terminal: Oh My Zsh"
if [ -d ~/.oh-my-zsh ]; then
    echo "Oh My Zsh is already installed"
    sleep 1
else
    echo "Installing Oh My Zsh"
    sleep 1
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    echo "Oh My Zsh is installed"
    sleep 1
fi
echo ""

#h! Terminal: Architeture #####################################################
frame_text "Terminal: Architeture"
sleep 1

ZSHRC_ARCHITETURE='# ------------------------------------------------------------------------------
# Architeture
# ------------------------------------------------------------------------------
if [ "$(uname -p)" = "i386" ]; then
    # echo "Running in i386 mode (Rosetta)"
    # eval "$(/usr/local/homebrew/bin/brew shellenv)"
    eval "$(/usr/local/bin/brew shellenv)"
    alias brew="/usr/local/bin/brew"
else
    # echo "Running in ARM mode (M1/M2)"
    eval "$(/opt/homebrew/bin/brew shellenv)"
    alias brew="/opt/homebrew/bin/brew"
fi'

if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_ARCHITETURE"* ]]; then
    echo "Appending Architeture settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$ZSHRC_ARCHITETURE" >>~/.zshrc
else
    echo "Architeture settings are already appended"
fi
echo ""

#h! Terminal: Powerlevel10k ###################################################
frame_text "Terminal: Powerlevel10k"
sleep 1
if brew list --formula | grep -q "powerlevel10k"; then
    echo "Powerlevel10k is already installed"
else
    echo "Installing Powerlevel10k"
    brew install romkatv/powerlevel10k/powerlevel10k
    echo "Powerlevel10k is installed"
fi
echo ""

#h! Terminal: Configure Powerlevel10k #########################################
frame_text "Terminal: Configure Powerlevel10k"
sleep 1

ZSHRC_POWERLEWEL10K='# ------------------------------------------------------------------------------
# Powerlevel10k
# ------------------------------------------------------------------------------
# Set Powerlevel10k theme.
source $(brew --prefix powerlevel10k)/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh'

if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_POWERLEWEL10K"* ]]; then
    echo "Appending Powerlevel10k settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$ZSHRC_POWERLEWEL10K" >>~/.zshrc
else
    echo "Powerlevel10k settings already in .zshrc"
fi
echo ""

set -e
if ! brew list --formula | grep -q "powerlevel10k"; then
    echo "Powerlevel10k is not installed. Aborting..."
    exit 1
fi

if [ ! -f ~/.p10k.zsh ]; then
    echo "\n\n"
    frame_multiline_text "Powerlevel10k is not configured. However, you need to manually continue the installation process.
To do this run: 'sh install.sh'"
    sleep 5
    exec zsh
else
    echo "File '.p10k.zsh' already exists..."
fi
echo ""

read -p "Do you want to apply the custom modifications to the file? [y/N] " -n 1 -r REPLY
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "\nAborting...\n"
else
    echo ""
    echo "Applying custom modifications to the file...\n"
    sh configure_p10k.sh
    echo "\nCustom modifications applied to the file..."
fi
echo ""

#h! Terminal: zsh-syntax-highlighting #########################################
frame_text "Terminal: zsh-syntax-highlighting"

if brew list --formula | grep -q "zsh-syntax-highlighting"; then
    echo "zsh-syntax-highlighting is already installed"
else
    echo "Installing zsh-syntax-highlighting"
    brew install zsh-syntax-highlighting
    echo "zsh-syntax-highlighting is installed"
fi

ZSHRC_ZSH_SYNTAX_HIGHLIGHTING='# ------------------------------------------------------------------------------
# zsh-syntax-highlighting
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh'

if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_ZSH_SYNTAX_HIGHLIGHTING"* ]]; then
    echo "Appending zsh-syntax-highlighting settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$ZSHRC_ZSH_SYNTAX_HIGHLIGHTING" >>~/.zshrc
else
    echo "zsh-syntax-highlighting settings already in .zshrc"
fi
echo ""

#h! Terminal: zsh-autosuggestions #############################################
frame_text "Terminal: zsh-autosuggestions"

if brew list --formula | grep -q "zsh-autosuggestions"; then
    echo "zsh-autosuggestions is already installed"
else
    echo "Installing zsh-autosuggestions"
    brew install zsh-autosuggestions
    echo "zsh-autosuggestions is installed"
fi

ZSHRC_ZSH_AUTOSUGGESTIONS='# ------------------------------------------------------------------------------
# zsh-autosuggestions
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh'

if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_ZSH_AUTOSUGGESTIONS"* ]]; then
    echo "Appending zsh-autosuggestions settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$ZSHRC_ZSH_AUTOSUGGESTIONS" >>~/.zshrc
else
    echo "zsh-autosuggestions settings already in .zshrc"
fi
echo ""

#h! Terminal: zsh-autoswitch-virtualenv #######################################
frame_text "Terminal: zsh-autoswitch-virtualenv"
sleep 1

ZSH_CUSTOM="$HOME/.oh-my-zsh/custom"
FILE="$ZSH_CUSTOM/plugins/autoswitch_virtualenv/autoswitch_virtualenv.plugin.zsh"
FUNCTION="function _autoswitch_startup() {"
SNIPPET="autoload -Uz add-zsh-hook
enable_autoswitch_virtualenv
check_venv
"

if ! [ -f "$FILE" ]; then
    git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "$ZSH_CUSTOM/plugins/autoswitch_virtualenv"
    echo ""
    echo "zsh-autoswitch-virtualenv is installed"
    sleep 1

    if [ -f "$FILE" ]; then
        if grep -qF "$FUNCTION" "$FILE"; then
            line_number=$(grep -n "$FUNCTION" "$FILE" | cut -d: -f1)
            line remove range "$line_number" to end in $FILE
            printf "%s\n" "$SNIPPET" >>"$FILE"
            echo "Modified:     Temporary fix for zsh-autoswitch-virtualenv and pyenv implemented"
        else
            echo "Not found:    $FILE does not contain the function that needs to be replaced"
        fi
    else
        echo "Not found:    $FILE does not exist"
    fi
else
    echo "zsh-autoswitch-virtualenv is already installed"
fi
sleep 1
echo ""

#h! Terminal: plugins #########################################################
frame_text "Terminal: plugins"
sleep 1

line replace first "plugins=(git)" with "plugins=(autoswitch_virtualenv brew git gh wd dotnet vscode poetry docker docker-compose)" in ~/.zshrc

#h! Terminal: warp drive ######################################################
frame_text "Terminal: warp drive"
sleep 1

if [ ! -f ~/.warprc ]; then
    touch ~/.warprc
fi

LINES="dev:~/Documents/Development
puzzel:~/Puzzel
home:~
repo:~/Documents/Development/Projects/Repository"

while IFS= read -r line; do
    if [[ "$(cat ~/.warprc)" != *"$line"* ]]; then
        echo "Appending $line to ~/.warprc"

        if [ "$(tail -c 1 ~/.warprc)" != "" ]; then
            echo "" >>~/.warprc
        fi
        echo "$line" >>~/.warprc
    else
        echo "Setting $line already exists in ~/.warprc"
    fi
done <<<"$LINES"
echo ""

#h! Terminal: pyenv ###########################################################
frame_text "Terminal: pyenv"
sleep 1

if brew list --formula | grep -q "pyenv"; then
    echo "pyenv is already installed"
else
    echo "Installing pyenv"
    brew install pyenv
    echo "pyenv is installed"
fi

if brew list --formula | grep -q "pyenv-virtualenv"; then
    echo "pyenv-virtualenv is already installed"
else
    echo "Installing pyenv-virtualenv"
    brew install pyenv-virtualenv
    echo "pyenv-virtualenv is installed"
fi

PYENV='# ------------------------------------------------------------------------------
# pyenv
# ------------------------------------------------------------------------------
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"'

if [[ "$(cat ~/.zshrc)" != *"$PYENV"* ]]; then
    echo "Appending pyenv settings to .zshrc"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$PYENV" >>~/.zshrc
else
    echo "pyenv settings already in .zshrc"
fi

if [[ "$(cat ~/.zprofile)" != *"$PYENV"* ]]; then
    echo "Appending pyenv settings to .zprofile"
    if [ -s ~/.zprofile ]; then
        if [ "$(tail -c 1 ~/.zprofile)" != "" ]; then
            echo "\n" >>~/.zprofile
        else
            echo "" >>~/.zprofile
        fi
    fi
    echo "$PYENV" >>~/.zprofile
else
    echo "pyenv settings already in .zprofile"
fi
echo ""

#h! Terminal: Poetry ##########################################################
frame_text "Terminal: Poetry"
sleep 1
# export PATH="/Users/lewiuberg/.local/bin:$PATH"
POETRY='# ------------------------------------------------------------------------------
# Poetry
# ------------------------------------------------------------------------------
export PATH="$HOME/.local/bin:$PATH"'

# TODO: This may be the solution if there are issues with poetry
# fpath+=~/.zfunc
# autoload -Uz compinit && compinit

# if poetry does not exsist in /Users/lewiuberg/.local/bin, install it
if [ ! -f ~/.local/bin/poetry ]; then
    echo "Installing Poetry"
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry is installed"
else
    echo "Poetry is already installed"
fi

if [[ "$(cat ~/.zshrc)" != *"$POETRY"* ]]; then
    echo "Appending Poetry settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$POETRY" >>~/.zshrc
else
    echo "Poetry settings already in .zshrc"
fi

if [ ! -L ~/.virtualenvs-alias-poetry ]; then
    echo "Creating alias for Poetry virtualenvs"
    ln -s "$HOME/Library/Caches/pypoetry/virtualenvs" ~/.virtualenvs-alias-poetry
    echo "Alias created"
else
    echo "Alias for Poetry virtualenvs already exists"
fi

export PATH="$HOME/.local/bin:$PATH"
# Make poetry use the active python version. Like pyenv local 3.8.2
poetry config virtualenvs.prefer-active-python true
echo ""

#h! Terminal; Direnv ##########################################################
frame_text "Terminal: Direnv"
sleep 1

DIRENV='# ------------------------------------------------------------------------------
# Direnv
# ------------------------------------------------------------------------------
eval "$(direnv hook zsh)"
export EDITOR="code --wait"'

if brew list --formula | grep -q "direnv"; then
    echo "direnv is already installed"
else
    echo "Installing direnv"
    brew install direnv
    echo "direnv is installed"
fi

if [[ "$(cat ~/.zshrc)" != *"$DIRENV"* ]]; then
    echo "Appending direnv settings"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$DIRENV" >>~/.zshrc
else
    echo "direnv settings already in .zshrc"
fi
echo ""

#h! Terminal: Dotnet-sdk ######################################################
frame_text "Terminal: Dotnet-sdk"
sleep 1

# check if dotnet-sdk is installed
if brew list --formula | grep -q "dotnet-sdk"; then
    echo "dotnet-sdk is already installed"
else
    # brew install spesific version of dotnet-sdk
    formula_file_to_download="https://raw.githubusercontent.com/Homebrew/homebrew-cask/e5fdbb2d63b55aec9393bfd64048a6826e78a80b/Casks/dotnet-sdk.rb"
    # Download the formula file to ~/Downloads if it does not exsist
    if [ ! -f ~/Downloads/dotnet-sdk.rb ]; then
        echo "Downloading dotnet-sdk.rb"
        curl -o ~/Downloads/dotnet-sdk.rb $formula_file_to_download
        echo "dotnet-sdk.rb downloaded"
    fi

    echo "Installing dotnet-sdk"
    cd ~/Downloads
    brew install --cask dotnet-sdk.rb
    cd -
    echo "dotnet-sdk is installed"
fi

#! Not yet working as expected
# DOTNET_VERSION="dotnet-sdk6-0-400"
# # check if dotnet-sdk is installed via brew
# if brew list --cask | grep -q "$DOTNET_VERSION"; then
#     echo "$DOTNET_VERSION is already installed"
# else
#     # install dotnet-sdk via brew
#     echo "Installing $DOTNET_VERSION"
#     brew tap isen-ng/dotnet-sdk-versions
#     brew install --cask $DOTNET_VERSION
#     echo "$DOTNET_VERSION is installed"
# fi
#! Not yet working as expected

# export DOTNET_ROOT=$HOME/dotnet
#export DOTNET_ROOT=/usr/local/bin/dotnet

# in zprofile
#! export PATH="$PATH:/Users/lewiuberg/.dotnet/tools"
echo ""

#h! Terminal: Azure Artifact Credential Provider ##############################
frame_text "Terminal: Azure Artifact Credential Provider"
sleep 1

if [ -d ~/.nuget/plugins/netcore/CredentialProvider.Microsoft ]; then
    echo "azure-artifact-credential-provider is already installed"
else
    echo "Installing azure-artifact-credential-provider"
    sh -c "$(curl -fsSL https://aka.ms/install-artifacts-credprovider.sh)"
    echo "azure-artifact-credential-provider is installed"
    echo "\n"
    read -p "The first time you open a dotnet project, you need to restore interactivally.\n\n dotnet restore --interactive\n\nPress enter to continue"
fi
echo ""

#h! Terminal: Aliases #########################################################
frame_text "Terminal: Aliases"
sleep 1

ALIASES='# ------------------------------------------------------------------------------
# Aliases
# ------------------------------------------------------------------------------
alias azsh="arch -arm64 zsh" # Run zsh in ARM mode
alias izsh="arch -x86_64 zsh" # Run zsh in i386 mode
alias aliases="grep \"^alias\" ~/.zshrc | sed \"s/alias //g\"" # list all aliases
alias lss="ls -alhS" # list files by size
alias lsla="ls -la" # list all files including hidden
alias ch="history | grep \"git commit\"" # list all git commits
alias pih="history | grep \"pip install\"" # list all pip installs
alias poh="history | grep \"poetry add\"" # list all poetry installs
alias hg="history | grep" # search history
alias ppip="python3 -m pip" # pip3
alias show="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder" # show hidden files
alias hide="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder" # hide hidden files
alias back="cd .. && echo "" && cd -" # go back to previous directory'

if [[ "$(cat ~/.zshrc)" != *"$ALIASES"* ]]; then
    echo "Appending aliases"
    if [ -s ~/.zshrc ]; then
        if [ "$(tail -c 1 ~/.zshrc)" != "" ]; then
            echo "\n" >>~/.zshrc
        else
            echo "" >>~/.zshrc
        fi
    fi
    echo "$ALIASES" >>~/.zshrc
else
    echo "Aliases already in .zshrc"
fi
echo ""
