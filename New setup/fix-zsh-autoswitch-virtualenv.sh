#!/usr/bin/env zsh

source functions.sh
source constants.sh

ZSH_CUSTOM="$HOME/.oh-my-zsh/custom"
FILE="$ZSH_CUSTOM/plugins/autoswitch_virtualenv/autoswitch_virtualenv.plugin.zsh"

FUNCTION="function _autoswitch_startup() {"
SNIPPET="function _autoswitch_startup() {
    if ! type \"python\" > /dev/null; then
        printf \"WARNING: python binary not found on PATH.\n\"
        printf \"zsh-autoswitch-virtualenv plugin will be disabled.\n\"
    else
        add-zsh-hook -D precmd _autoswitch_startup
        enable_autoswitch_virtualenv
        check_venv
    fi
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd _autoswitch_startup"

# Terminal: Zsh Autoswitch Virtualenv ###########################################
frame_text "Terminal: Zsh Autoswitch Virtualenv"
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
echo ""
