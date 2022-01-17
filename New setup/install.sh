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
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew doctor
brew install cask
echo 'export PATH="/usr/local/sbin:$PATH"' >>~/.zshrc
source "${homedir}"/dotfiles/.zshrc
brew doctor
# homebrew cask updater: https://github.com/buo/homebrew-cask-upgrade
brew tap buo/cask-upgrade

# Run the Terminal Script
./terminal.sh

# Run the Homebrew Script
./brew.sh

# Setup Git
git config --global user.name "Lewi Uberg"
git config --global user.email "lewiuberg@icloud.com"
git config --global init.defaultBranch main
git config --global -l

# Setup SSH
cd ~/.ssh

echo "Generating keys."
echo ""

ssh-keygen -t ed25519 -C "lewiuberg@icloud.com" -f "lewiuberg@icloud.com"
pbcopy < ~/.ssh/lewiuberg@icloud.com.pub
open https://github.com/settings/ssh/new

echo ""

ssh-keygen -t ed25519 -C "lewi@anzyz.com" -f "lewi@anzyz.com"
pbcopy < ~/.ssh/lewi@anzyz.com.pub
open https://bitbucket.org/account/settings/ssh-keys/

echo ""
echo "Setup ssh config file."

touch ~/.ssh/config

printf '%s\n' \
    "# Personal" \
    "Host github.com" \
    "HostName github.com" \
    "User git" \
    "IdentityFile ~/.ssh/lewiuberg@icloud.com" \
    "UseKeychain yes" \
    "AddKeysToAgent yes" \
    "" \
    "# Work" \
    "Host bitbucket.org" \
    "HostName bitbucket.org" \
    "User git" \
    "IdentityFile ~/.ssh/lewi@anzyz.com" \
    "UseKeychain yes" \
    "AddKeysToAgent yes" \
    >>~/.ssh/config

cat ~/.ssh/config
echo ""

echo ""
echo "Add identities."
echo ""

ssh-add --apple-use-keychain ~/.ssh/lewiuberg@icloud.com
ssh-add --apple-use-keychain ~/.ssh/lewi@anzyz.com

ssh-add -l

echo ""
echo "Add to known hosts."

ssh-keyscan github.com >> ~/.ssh/known_hosts
ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts

echo ""
echo "Test connection."
read -n 1 -s -r -p "Press any key to continue..."
echo ""

ssh -T github.com
ssh -T bitbucket.org

echo ""
echo "Use [git config user.name 'Lewi Uberg'] and [git config user.email lewi@anzyz.com] at repo level to ensure secondary host."
echo "For more information, see: https://gist.github.com/rosswd/e1afd2b0b0d515517eac"

cd ~

# Run the VScode extension Script
./vscode_extensions.sh
