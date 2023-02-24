![](https://visitor-badge.glitch.me/badge?page_id=lewiuberg.Setup)

# Setup

This repository contains scripts I use for a new macOS setup, template for a new general project, or custom project templates.

# Rosetta

sudo softwareupdate --install-rosetta

# Homebrew

Install Homebrew on your Mac by running the following command in your terminal:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Edit .zprofile

Add the following line to your .zprofile file:

```sh
echo '# Set PATH, MANPATH, etc., for Homebrew.' >> /Users/lewiuberg/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/lewiuberg/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

New

```sh
# ------------------------------------------------------------------------------
# Homebrew
# ------------------------------------------------------------------------------
# Set PATH, MANPATH, etc., for Homebrew.
eval "$(/opt/homebrew/bin/brew shellenv)"
```

The file should now look like this:

```text
# ------------------------------------------------------------------------------
# Homebrew
# ------------------------------------------------------------------------------
# Set PATH, MANPATH, etc., for Homebrew.
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Then run `eval "$(/opt/homebrew/bin/brew shellenv)"` in your terminal to update your environment variables.

## Install homebrew packages

Start by updating homebrew:

```bash
brew update
```

Then install the following packages:

```bash
#!/usr/bin/env zsh

# Install Brew Packages
brew install tree # tree view
brew install smudge/smudge/nightlight # nightlight
brew install git # git
brew install git-lfs # git large file storage
brew install gh # github cli
brew install azure-cli # azure
brew install pyenv # python
brew install pyenv-virtualenv # pyenv virtualenv
brew install node # nodejs
brew install graphviz # for graphviz
brew install lcov # code coverage
brew install lnav # log viewer
# brew install pwgen # password generator
# brew install virtualenv
# brew install direnv
# brew install docker-machine

# https://github.com/isen-ng/homebrew-dotnet-sdk-versions
brew install dotnet-sdk
brew tap isen-ng/dotnet-sdk-versions
brew install --cask dotnet-sdk6-0-400

# Install MacOS Applications
brew install --cask syntax-highlight
brew install --cask parallels
brew install --cask parallels-access
brew install --cask parallels-client
brew install --cask parallels-toolbox
brew install --cask vnc-viewer
brew install --cask termius
brew install --cask transmission-cli
brew install --cask avast-security
brew install --cask prince
brew install --cask unite
brew install --cask visual-studio-code
brew install --cask azure-data-studio
brew install --cask gitkraken
# brew install --cask github
# brew install --cask sourcetree
# brew install --cask fork
brew install --cask docker
brew install --cask postman
brew install --cask notion
brew install --cask slack
brew install --cask discord
brew install --cask messenger
brew install --cask workplace-chat
brew install --cask grammarly
brew install --cask grammarly-desktop
brew install --cask microsoft-office
brew install --cask microsoft-teams

brew tap homebrew/cask-fonts && brew install --cask font-meslo-lg-nerd-font
brew install --cask google-chrome
brew install --cask jetbrains-toolbox
brew install --cask rider
brew install --cask sdformatter
brew install --cask raspberry-pi-imager
brew install --cask balenaetcher
brew install --cask applepi-baker
brew install --cask jupyter-notebook-viewer
brew install --cask qlmarkdown

brew install --cask qlstephen
brew install --cask autodesk-fusion360
brew install --cask blender
brew install --cask tableplus
brew install --cask betterzip

brew install --cask unite
brew install --cask sketchbook
brew install --cask microsoft-remote-desktop



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
```

# Terminal

Install Oh-my-zs

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Install PowerLevel10k

```bash
brew install romkatv/powerlevel10k/powerlevel10k
echo 'source $(brew --prefix powerlevel10k)/powerlevel10k.zsh-theme' >>! ~/.zshrc
```

# App store

install

- [BetterJSON](https://apps.apple.com/no/app/betterjson-for-safari/id1511935951?l=nb&mt=12)
- [BetterSnapTool](https://apps.apple.com/no/app/bettersnaptool/id417375580?l=nb&mt=12)
- [Dark Reader For Safari](https://apps.apple.com/no/app/dark-reader-for-safari/id1438243180?l=nb)
- [Dynamo](https://apps.apple.com/no/app/dynamo/id1445910651?l=nb&mt=12)
- [Graphic](https://apps.apple.com/no/app/graphic/id404705039?l=nb&mt=12)
- [HP Easy Scan](https://apps.apple.com/no/app/hp-easy-scan/id967004861?l=nb&mt=12)
- [iStatistica Pro](https://apps.apple.com/no/app/istatistica-pro/id1447778660?l=nb&mt=12)
- [LanScan](https://apps.apple.com/no/app/lanscan/id472226235?l=nb&mt=12)
- [Mac Server](https://apps.apple.com/no/app/macos-server/id883878097?l=nb&mt=12)
- [New File Menu](https://apps.apple.com/no/app/new-file-menu/id1064959555?l=nb&mt=12)
- [Parcel](https://apps.apple.com/no/app/parcel-delivery-tracking/id639968404?l=nb&mt=12)
- [RAR Extractor - Unarchiver Pro](https://apps.apple.com/no/app/rar-extractor-unarchiver-pro/id647505820?l=nb&mt=12)
- [Ring](https://apps.apple.com/no/app/ring-always-home/id1142753258?l=nb&mt=12)
- [Smart Converter Pro 2](https://apps.apple.com/no/app/smart-converter-pro-2/id660234210?l=nb&mt=12)
- [Viper FTP Lite](https://apps.apple.com/no/app/viper-ftp-lite/id1001007066?l=nb&mt=12)

# Apple Silicon

Apple is transitioning to a new silicon architecture and more and more software is starting to support it. However transitioning to a new silicon architecture takes time, and there is still much software that is not yet ready to support it. This is where the Rosetta2 translation layer is applicable. Rosetta2 is a translation layer that emulates x86 and allows you to use the new silicon architecture without having to change your code.

If you are using Homebrew and Pyenv for example you will need to use both rosetta and a dedicated x86 version of homebrew. Managing all this can be confusing and cumbersome. To make It a little easier, consider implementing the changes described below.

## Install Rosetta2

Open the terminal and run the following command:

```bash
softwareupdate —-install-rosetta
```

## Modify .zshrc

Many articles online suggest making a copy of the terminal and modifying it to be the Rosetta2 version. However, this is not necessary. It is a much better idea to be able to switch back and forth between the two versions in the same terminal.

Add the following line to your .zshrc file:

```sh
alias azsh="arch -arm64 zsh"
alias izsh="arch -x86_64 zsh"

if [ "$(uname -p)" = "i386" ]; then
  echo "Running in i386 mode (Rosetta)"
  eval "$(/usr/local/homebrew/bin/brew shellenv)"
  # alias brew='/usr/local/homebrew/bin/brew'
  alias brew="/usr/local/bin/brew"
else
  echo "Running in ARM mode (M1)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
  alias brew="/opt/homebrew/bin/brew"
fi
```

Now you can switch between to the rosetta terminal by running the following command:

```bash
izsh
```

or to the Apple Silicon terminal by running the following command:

```bash
azsh
```

## Oh-my-zsh and Powerlevel10k

If you are using Oh-my-zsh and Powerlevel10k, you can have the prompt show the current terminal. To do this you need to swap the following lines in your .p10k.zsh:

```sh
typeset -g POWERLEVEL9K_PROMPT_CHAR_{OK,ERROR}_VIINS_CONTENT_EXPANSION='❯'
```

with

```sh
typeset -g POWERLEVEL9K_PROMPT_CHAR_{OK,ERROR}_VIINS_CONTENT_EXPANSION='$(arch) ❯'
```

## Install x86 Homebrew

Open your terminal and run the following commands:

```bash
izsh
```

then

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
