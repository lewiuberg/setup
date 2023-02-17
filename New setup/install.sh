#!/usr/bin/env zsh
###############################################################################
# This script installs Homebrew Packages, OhMyZsh, Powerlevel10k and VS Code extensions.
# It also changes the settings for .zshrc, .zprofile, .p10k.zsh and more.
###############################################################################
clear
source functions.sh
source constants.sh

# Information #################################################################
frame_text "Setting up new Mac"
frame_text "Information"
echo "User: ${USER}"
echo "Home directory path: ${HOMEDIR}"
if [ "$ARCH_ARM64" = true ]; then
    echo "Architecture: arm64"
elif [ "$ARCH_86_64" = true ]; then
    echo "Architecture: x86_64"
fi

# if .zprofile does not exist, create it
if [ ! -f ~/.zprofile ]; then
    touch ~/.zprofile
    echo "Created .zprofile"
fi

# if .zshrc does not exist, create it
if [ ! -f ~/.zshrc ]; then
    touch ~/.zshrc
    echo "Created .zshrc"
fi

echo ""

# Rosetta 2 ###################################################################
sleep 1
frame_text "Rosetta 2"

if [ "$ARCH_ARM64" = true ]; then
    if [[ "$(pkgutil --files com.apple.pkg.RosettaUpdateAuto)" == "" ]]; then
        echo "Installing Rosetta 2"
        sudo softwareupdate --install-rosetta --agree-to-license
    else
        echo "Rosetta 2 is already installed"
    fi
elif [ "$ARCH_86_64" = true ]; then
    echo "Rosetta 2 is not needed"
else
    echo "Unknown ARCHITECTURE"
fi

echo ""

# Homebrew ####################################################################
sh brew.sh

# Terminal ####################################################################
sh terminal.sh

# App Store ###################################################################
sh manual_installations.sh
