#!/usr/bin/env zsh

source functions.sh
source constants.sh

# Terminal ####################################################################
sleep 1
frame_text "Terminal"

# Terminal: Oh My Zsh ##########################################################
frame_text "Terminal: Oh My Zsh"
if [ -d ~/.oh-my-zsh ]; then
    echo "Oh My Zsh is already installed"
else
    echo "Installing Oh My Zsh"
    #! sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    echo "Oh My Zsh is installed"
fi
echo ""

# Terminal: Powerlevel10k ######################################################
frame_text "Terminal: Powerlevel10k"
if [ -f ~/.p10k.zsh ]; then
    echo "Powerlevel10k is already installed"
else
    echo "Installing Powerlevel10k"
    brew install romkatv/powerlevel10k/powerlevel10k
    echo "Powerlevel10k is installed"
fi

ZSHRC_POWERLEWEL10K='# ------------------------------------------------------------------------------
# Powerlevel10k
# ------------------------------------------------------------------------------
# Set Powerlevel10k theme.
source $(brew --prefix powerlevel10k)/powerlevel10k.zsh-theme'

# check if ZSHRC_POWERLEWEL10K is in .zshrc
if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_POWERLEWEL10K"* ]]; then
    echo "Appending Powerlevel10k settings"
    # check if file is empty
    if [ -s ~/.zshrc ]; then
        # check if last line is empty, if not, add an empty line
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
