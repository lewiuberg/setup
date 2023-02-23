#!/usr/bin/env zsh

source functions.sh
source constants.sh

# Terminal ####################################################################
sleep 1
frame_text "Terminal"
echo ""

# echo "1? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

# Terminal: Oh My Zsh ##########################################################
frame_text "Terminal: Oh My Zsh"
if [ -d ~/.oh-my-zsh ]; then
    echo "Oh My Zsh is already installed"
else
    # ask the user if they want to install Oh My Zsh, store reply in variable, if not, exit and move on
    #     read -p "Oh My Zsh is not installed!
    # Do you want to install Oh My Zsh? [y/N] " -n 1 -r answer
    #     echo "Oh My Zsh is not installed!
    # Do you want to install Oh My Zsh? [y/N]"
    #     read -k1 "?"
    #     if [[ $REPLY =~ ^[Yy]$ ]]; then
    #     read -p "Oh My Zsh is not installed!
    # Do you want to install Oh My Zsh? [y/N] " -n 1 -r
    #     if [[ $REPLY =~ ^[Yy]$ ]]; then
    # echo ""
    # frame_text "OBS! After configuration, you will need to run the install script again."
    # echo ""
    sleep 5
    echo "Installing Oh My Zsh"
    # sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    # sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sed 's:env zsh::g' | sed 's:chsh -s .*$::g')"
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    echo "Oh My Zsh is installed"
    # else
    #     echo "Oh My Zsh is not installed"
    #     exit 1
    # fi
fi
echo ""

# echo "2? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

# Terminal: Powerlevel10k ######################################################
frame_text "Terminal: Powerlevel10k"
if brew list --formula | grep -q "powerlevel10k"; then
    echo "Powerlevel10k is already installed"
else
    echo "Installing Powerlevel10k"
    brew install romkatv/powerlevel10k/powerlevel10k
    echo "Powerlevel10k is installed"
fi
echo ""

# echo "3? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

# Terminal: Configure Powerlevel10k ############################################
frame_text "Terminal: Configure Powerlevel10k"

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

set -e
if ! brew list --formula | grep -q "powerlevel10k"; then
    echo "Powerlevel10k is not installed. Aborting..."
    exit 1
fi

if [ ! -f ~/.p10k.zsh ]; then
    echo "File '.p10k.zsh' does not exist. Running 'p10k configure'...\n"
    echo "Powerlevel10k is not configured. Please run 'p10k configure' and then run 'zsh install.sh' again."
    exec zsh
else
    echo "File '.p10k.zsh' exists. Continuing..."
    echo ""
fi

# read -k1 "?Do you want to apply the custom modifications to the file? [y/N] "
read -p "Do you want to apply the custom modifications to the file? [y/N] " -n 1 -r REPLY
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "\nAborting..."
    echo ""
    exit 1
else
    echo "\nApplying custom modifications to the file..."
    echo ""
    sh configure_p10k.sh
fi

# zsh configure_p10k.sh

read -p "Do you wish to continue? [y/N] " -n 1 -r
# echo "4? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

# Terminal: zsh-syntax-highlighting ############################################
frame_text "Terminal: zsh-syntax-highlighting"

ZSHRC_ZSH_SYNTAX_HIGHLIGHTING='# ------------------------------------------------------------------------------
# zsh-syntax-highlighting
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh'

# check if ZSHRC_ZSH_SYNTAX_HIGHLIGHTING is in .zshrc
if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_ZSH_SYNTAX_HIGHLIGHTING"* ]]; then
    echo "Appending zsh-syntax-highlighting settings"
    # check if file is empty
    if [ -s ~/.zshrc ]; then
        # check if last line is empty, if not, add an empty line
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

echo "6? [y/N]" #! LEWI
read -k1 -s "?" #! LEWI

# Terminal: zsh-autosuggestions ###############################################
frame_text "Terminal: zsh-autosuggestions"

ZSHRC_ZSH_AUTOSUGGESTIONS='# ------------------------------------------------------------------------------
# zsh-autosuggestions
# ------------------------------------------------------------------------------
source $HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh'

# check if ZSHRC_ZSH_AUTOSUGGESTIONS is in .zshrc
if [[ "$(cat ~/.zshrc)" != *"$ZSHRC_ZSH_AUTOSUGGESTIONS"* ]]; then
    echo "Appending zsh-autosuggestions settings"
    # check if file is empty
    if [ -s ~/.zshrc ]; then
        # check if last line is empty, if not, add an empty line
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

echo "7? [y/N]" #! LEWI
read -k1 -s "?" #! LEWI

# zsh-autoswitch-virtualenv
# git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "$ZSH_CUSTOM/plugins/autoswitch_virtualenv"
# # Update .zshrc to activate autoswitch-virtualenv
# # ! sed -i '' 's/# Add wisely, as too many plugins slow down shell startup./# Add wisely, as too many plugins slow down shell startup.\nplugins=(autoswitch_virtualenv brew git poetry vscode docker docker-compose)\n/n/g' ~/.zshrc

# plugins

# pyenv

# warp drive
