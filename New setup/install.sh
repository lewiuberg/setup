#!/usr/bin/env zsh
################################################################################
# This script creates symlinks from the home directory to any desired Scripts in ${homedir}/Scripts
# And also installs Homebrew Packages, OhMyZsh, Powerlevel10k and VS Code extensions
################################################################################

clear

if [ "$#" -ne 1 ]; then
    echo "Usage: install.sh <user_account>"
    exit 1
fi

# Making path variables
echo "[Dot files]"
echo
# User account
user="$1"
echo "User: ${user}"
# Scripts directory
#filesdir=$(echo "$PWD" | sed "s/ /\\\ /g")
filesdir=$PWD
echo "Installation files path: ${filesdir}"
cd
# Home directory
#homedir=$(echo "$PWD" | sed -r -e "s/ /\\\ /g")
homedir=$PWD
echo "Home directory path: ${homedir}"
echo
# Make folder for dotfiles in the home directory
echo "List of files to symlink in: ${homedir}"
files="zshrc"
echo $files
echo
echo "Making folder for dotfiles: ${homedir}/dotfiles"
mkdir -p ${homedir}/dotfiles
echo "Copying files to: ${homedir}/dotfiles"
cp "$filesdir"/.${files} ${homedir}/dotfiles
cd "$filesdir"
pwd
# create symlinks (will overwrite old Scripts)
for file in ${files}; do
    echo "Creating symlink to $file in home directory."
    ln -sf ${homedir}/dotfiles/.${file} ${homedir}/.${file}
done

echo
source "${homedir}"/dotfiles/.zshrc
echo ""
echo "[Done]"
echo ""

# Install Homebrew
curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh
brew doctor
brew install cask
brew doctor
# homebrew cask updater: https://github.com/buo/homebrew-cask-upgrade
brew tap buo/cask-upgrade

# Download Git Auto-Completion
curl "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash" > ${homedir}/.git-completion.bash

# Run the Terminal Script
./terminal.sh

# Run the Homebrew Script
./brew.sh

# Run the VScode extension Script
./vscode_extensions.sh
