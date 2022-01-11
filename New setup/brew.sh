#!/usr/bin/env zsh

# Install Brew Packages
brew install pwgen
brew install node
brew install virtualenv
brew install pyenv
brew install pyenv-virtualenv
brew install git
brew install git-lfs
brew install gh
brew install tree
brew install graphviz
brew install smudge/smudge/nightlight
brew install direnv
brew install docker-machine
brew install azure-cli

# Install MacOS Applications
brew install --cask iterm2
brew install --cask syntax-highlight
brew install --cask qlmarkdown
brew install --cask qlstephen
brew install --cask parallels
brew install --cask parallels-access
brew install --cask parallels-client
brew install --cask parallels-toolbox
brew install --cask vnc-viewer
brew install --cask virtualbox
brew install --cask termius
brew install --cask transmission
brew install --cask fluid
brew install --cask avast-security
brew install --cask autodesk-fusion360
brew install --cask blender
brew install --cask visual-studio-code
brew install --cask prince
brew install --cask github
brew install --cask sourcetree
brew install --cask slack
brew install --cask discord
brew install --cask messenger
brew install --cask jabref
brew install --cask grammarly
brew install --cask grammarly-desktop
brew install --cask microsoft-office
brew install --cask microsoft-teams
brew install --cask docker
brew install --cask postman
brew install --cask notable
brew install --cask sdformatter
brew install --cask raspberry-pi-imager
brew install --cask balenaetcher
brew install --cask applepi-baker

# Install casks of drivers
brew tap homebrew/cask-drivers
brew install --cask logitech-options
brew install --cask philips-hue-sync

# Plugins for packages
# mkdir ~/.zfunc
# touch ~/.zfunc/_poetry
# poetry completions zsh > ~/.zfunc/_poetry

mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry
rm ~/.zcompdump*

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
echo "source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
