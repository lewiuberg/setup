#!/usr/bin/env zsh
################################################################################
# This script creates symlinks from the home directory to any desired Scripts in ${homedir}/Scripts
# And also installs Homebrew Packages
# And sets Sublime preferences
################################################################################

clear

if [ "$#" -ne 1 ]; then
    echo "Usage: install.sh <home_directory>"
    exit 1
fi

homedir=$1

# Scripts directory
scriptfiledir=${homedir}/Scripts

# list of files/folders to symlink in ${homedir}
files="zshrc"

# change to the Scripts directory
echo "Changing to the ${scriptfiledir} directory"
cd ${scriptfiledir}
echo "...done"

# create symlinks (will overwrite old Scripts)
for file in ${files}; do
    echo "Creating symlink to $file in home directory."
    ln -sf ${scriptfiledir}/.${file} ${homedir}/.${file}
done

source ${scriptfiledir}/.zshrc
echo ""
echo "[Sourced]"
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
