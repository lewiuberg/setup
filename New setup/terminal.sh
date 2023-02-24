#!/usr/bin/env zsh

source functions.sh
source constants.sh

#h! Terminal ####################################################################
frame_text "Terminal"
# sleep 1

# echo "1? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: Oh My Zsh ##########################################################
frame_text "Terminal: Oh My Zsh"
# sleep 1
if [ -d ~/.oh-my-zsh ]; then
    echo "Oh My Zsh is already installed"
    sleep 1
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
    echo "Installing Oh My Zsh"
    sleep 1
    # sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    # sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sed 's:env zsh::g' | sed 's:chsh -s .*$::g')"
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    echo "Oh My Zsh is installed"
    sleep 1
    # else
    #     echo "Oh My Zsh is not installed"
    #     exit 1
    # fi
fi
echo ""

# echo "2? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: Powerlevel10k ######################################################
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

# echo "3? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: Configure Powerlevel10k ############################################
frame_text "Terminal: Configure Powerlevel10k"
sleep 1

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
    # echo "File '.p10k.zsh' does not exist. Running 'p10k configure'...\n"
    # echo "Powerlevel10k is not configured. Please run 'p10k configure' and then run 'zsh install.sh' again."
    echo "\n\n"
    frame_multiline_text "Powerlevel10k is not configured. However, you need to manually continue the installation process.
To do this run: 'sh install.sh'"
    sleep 5
    exec zsh
else
    echo "File '.p10k.zsh' already exists..."
fi
echo ""

# read -k1 "?Do you want to apply the custom modifications to the file? [y/N] "
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

# zsh configure_p10k.sh

# read -p "Do you wish to continue? [y/N] " -n 1 -r REPLY
# # read -k1 "?Do you wish to continue? [y/N] "
# if [[ ! $REPLY =~ ^[Yy]$ ]]; then
#     echo "\nAborting...\n"
#     exit 1
# fi
# echo "4? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: zsh-syntax-highlighting ############################################
frame_text "Terminal: zsh-syntax-highlighting"

if brew list --formula | grep -q "zsh-syntax-highlighting"; then
    echo "zsh-syntax-highlighting is already installed"
else
    echo "Installing zsh-syntax-highlighting"
    brew install zsh-syntax-highlighting
    echo "zsh-syntax-highlighting is installed"
fi
echo ""

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
echo ""

# echo "6? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: zsh-autosuggestions ###############################################
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
echo ""

# echo "7? [y/N]" #! LEWI
# read -k1 -s "?" #! LEWI

#h! Terminal: zsh-autoswitch-virtualenv ########################################
frame_text "Terminal: zsh-autoswitch-virtualenv"
sleep 1

ZSH_CUSTOM="$HOME/.oh-my-zsh/custom"
FILE="$ZSH_CUSTOM/plugins/autoswitch_virtualenv/autoswitch_virtualenv.plugin.zsh"
FUNCTION="function _autoswitch_startup() {"
# SNIPPET="function _autoswitch_startup() {
#     if ! type \"python\" > /dev/null; then
#         printf \"WARNING: python binary not found on PATH.\n\"
#         printf \"zsh-autoswitch-virtualenv plugin will be disabled.\n\"
#     else
#         add-zsh-hook -D precmd _autoswitch_startup
#         enable_autoswitch_virtualenv
#         check_venv
#     fi
# }
# autoload -Uz add-zsh-hook
# add-zsh-hook precmd _autoswitch_startup"

SNIPPET="autoload -Uz add-zsh-hook
enable_autoswitch_virtualenv
check_venv
"
# # check if FILE exists
# if [ -f "$FILE" ]; then
#     # check if FUNCTION is in FILE
#     if grep -qF "$FUNCTION" "$FILE"; then
#         # find line with "function _autoswitch_startup() {" and echo line number
#         line_number=$(grep -n "$FUNCTION" "$FILE" | cut -d: -f1)
#         # remove line_number to end
#         line remove range "$line_number" to end in $FILE
#         # add SNIPPET to end of file
#         printf "%s\n" "$SNIPPET" >>"$FILE"
#         echo "Modified:     Temporary fix for zsh-autoswitch-virtualenv and pyenv implemented"
#     else
#         echo "Not found:    $FILE does not contain the function that needs to be replaced"
#     fi
# else
#     echo "Not found:    $FILE does not exist"
# fi

if ! [ -f "$FILE" ]; then
    git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "$ZSH_CUSTOM/plugins/autoswitch_virtualenv"
    echo ""
    echo "zsh-autoswitch-virtualenv is installed"
    sleep 1
    # check if FILE exists
    if [ -f "$FILE" ]; then
        # check if FUNCTION is in FILE
        if grep -qF "$FUNCTION" "$FILE"; then
            # find line with "function _autoswitch_startup() {" and echo line number
            line_number=$(grep -n "$FUNCTION" "$FILE" | cut -d: -f1)
            # remove line_number to end
            line remove range "$line_number" to end in $FILE
            # add SNIPPET to end of file
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

#h! Terminal: plugins ##########################################################
frame_text "Terminal: plugins"
sleep 1

line replace first "plugins=(git)" with "plugins=(autoswitch_virtualenv brew git gh wd dotnet vscode poetry docker docker-compose)" in ~/.zshrc

# pyenv

# warp drive
#h! Terminal: warp drive #######################################################
frame_text "Terminal: warp drive"
sleep 1
# if ~/.warprc does not exist, create it
if [ ! -f ~/.warprc ]; then
    touch ~/.warprc
fi
LINES="dev:~/Documents/Development
puzzel:~/Puzzel
home:~
repo:~/Documents/Development/Projects/Repository"
# check if LINES is in ~/.warp/warprc, if not, append it
# if [[ "$(cat ~/.warprc)" != *"$LINES"* ]]; then
#     echo "Appending warp drive settings"
#     # check if file is empty
#     if [ -s ~/.warprc ]; then
#         # check if last line is empty, if not, add an empty line
#         if [ "$(tail -c 1 ~/.warprc)" != "" ]; then
#             echo "\n" >>~/.warprc
#         else
#             echo "" >>~/.warprc
#         fi
#     fi
#     echo "$LINES" >>~/.warprc
# else
#     echo "warp drive settings already in ~/.warprc"
# fi
# echo ""

# split lines and check each line, if they do not exist, append them
while IFS= read -r line; do
    if [[ "$(cat ~/.warprc)" != *"$line"* ]]; then
        echo "Appending $line to ~/.warprc"
        # if current line in ~/.warprc is not empty, add an empty line
        if [ "$(tail -c 1 ~/.warprc)" != "" ]; then
            echo "" >>~/.warprc
        fi
        echo "$line" >>~/.warprc
    else
        # echo "warp drive settings already in ~/.warprc"
        echo "Setting $line already exists in ~/.warprc"
    fi
done <<<"$LINES"
echo ""
