#!/usr/bin/env zsh
source functions.sh
# check if homebrew has installed powerlevel10k, if not abort
frame_text "Powerlevel10k"
if ! brew list --formula | grep -q "powerlevel10k"; then
    echo "Powerlevel10k is not installed. Aborting..."
    exit 1
fi
# check if file '.p10k.zsh' exists at home directory, if not run 'p10k configure'
# if true, continue
if [ ! -f ~/.p10k.zsh ]; then
    echo "File '.p10k.zsh' does not exist. Running 'p10k configure'..."
    sleep 2
    #! p10k configure
    echo "p10k configure"
fi
# ask the user if they want to apply the custom modifications to the file. If not, abort
# if true, continue
read -p "Do you want to apply the custom modifications to the file? [y/N] " -n 1 -r

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "\nAborting..."
    echo ""
    exit 1
fi

echo "\nApplying custom modifications..."
line uncomment first "    # os_icon               # os identifier" in ~/.p10k.zsh
line add "    os_icon               # os identifier" below "    # =========================[ Line #1 ]=========================" in ~/.p10k.zsh
line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
# line uncomment first "    # newline               # \n" in ~/.p10k.zsh
line replace first "    # newline               # \n" with "    newline                 # \n" in ~/.p10k.zsh
line add "    newline                 # \n" below "    # prompt_char           # prompt symbol" in ~/.p10k.zsh
line comment first "    vi_mode                 # vi mode (you don't need this if you've enabled prompt_char)" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MODE=compatible" with "  typeset -g POWERLEVEL9K_MODE=nerdfont-complete" in ~/.p10k.zsh
# line check "$NEW_LINE" $WHERE "$NAVIGATION_LINE" $FILE_KEYWORD $FILE
#
#
#
# line check "    # os_icon               # os identifier" anywhere in ~/.p10k.zsh
# line check "    # os_icon               # os identifier" below "    # =========================[ Line #1 ]=========================" in ~/.p10k.zsh
# line remove line 41 from ~/.p10k.zsh
# line remove range 2 to 16 from ~/.p10k.zsh
# line remove range 1750 to end in ~/.p10k.zsh
# line remove range start to 3 from ~/.p10k.zsh
# line remove range start to end from ~/.p10k.zsh
# line remove all found "    # take me out           # \n\t" from ~/.p10k.zsh
# line remove first found "    # take me out           # \n\t" from ~/.p10k.zsh
# line remove last found "    # take me out           # \n\t" from ~/.p10k.zsh
# line replace all "    # newline               # \n" with "    newline1                # \n\t" in ~/.p10k.zsh
# line replace first "    # newline               # \n" with "    newline1                # \n\t" in ~/.p10k.zsh
# line comment first "    vcs                     # git status" in ~/.p10k.zsh
# line comment all "    vcs                     # git status" in ~/.p10k.zsh
# line uncomment first "    # os_icon               # os identifier" in ~/.p10k.zsh
# line uncomment first "    # newline               # \n" in ~/.p10k.zsh
# line comment all "    newline                 # \n" in ~/.p10k.zsh
# line uncomment all "    # newline               # \n" in ~/.p10k.zsh
# line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
# line add "    some new line # \n" above "    # prompt_char           # prompt symbol" in ~/.p10k.zsh
# line add "    # newline               # \n" below "    # newline               # \n" in ~/.p10k.zsh
# line add "    # newline               # \n" above "    # newline               # \n" in ~/.p10k.zsh
# POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
# line change "    # os_icon               # os identifier" to "    os_icon                 # os identifier" in ~/.p10k.zsh
# line add "    os_icon                 # os identifier" below "    # =========================[ Line #1 ]=========================" in ~/.p10k.zsh
# line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
# line change "    # prompt_char           # prompt symbol" to "    prompt_char             # prompt symbol" in ~/.p10k.zsh
# line add "    prompt_char             # prompt symbol" below "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh
# line change "    # newline               # \n" to "    newline                 # \n" in ~/.p10k.zsh
# line add "    newline                 # \n" below "    prompt_char             # prompt symbol" in ~/.p10k.zsh

# POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS
# line comment first "    vi_mode                 # vi mode (you don't need this if you've enabled prompt_char)" in ~/.p10k.zsh

# typeset -g POWERLEVEL9K_MODE
# line change "  typeset -g POWERLEVEL9K_MODE=compatible" to "  typeset -g POWERLEVEL9K_MODE=nerdfont-complete" in ~/.p10k.zsh

# line add "    Lewi was here" at start of ~/.p10k.zsh
# line add "    Lewi was here" at end of ~/.p10k.zsh

# line remove line 1765 from ~/.p10k.zsh
# line remove range 2 to 16 from ~/.p10k.zsh
# line remove range 1750 to end in ~/.p10k.zsh
# line remove range start to 3 from ~/.p10k.zsh
# line remove range start to end from ~/.p10k.zsh
# line remove all found "    Lewi was here" from ~/.p10k.zsh
# line remove first found "    Lewi was here" from ~/.p10k.zsh
# line remove last found "    Lewi was here" from ~/.p10k.zsh

# line append " # Lewi was here" to first "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh
# line append " # Lewi was here" to last "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh
# line append " # Lewi was here" to all "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh

#
#
#
# line change "    # os_icon               # os identifier" to "    os_icon                 # os identifier" in ~/.p10k.zsh
# line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
# line change "    # prompt_char           # prompt symbol" to "    prompt_char             # prompt symbol" in ~/.p10k.zsh
# line add "    prompt_char             # prompt symbol" below "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh
# line change "    # newline               # \\\n" to "    newline                 # \\\n" in ~/.p10k.zsh
# line add "    newline                 # \\\n" below "    # =========================[ Line #2 ]=========================" in ~/.p10k.zsh
# line change "    # newline               # \\\n" to "    newline                 # \\\n" in ~/.p10k.zsh
# line check "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh

# echo ""
# if [ $(line check "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh) -eq 0 ]; then
#     echo "Line exist"
# else
#     echo "Line does not exist"
#     line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
# fi
# echo ""
# if [ $(line check "    # =========================[ Line #2 ]=========================" above "    vcs                     # git status" in ~/.p10k.zsh) -eq 0 ]; then
#     echo "Line exist"
# else
#     echo "Line does not exist"
#     line add "    # =========================[ Line #2 ]=========================" above "    vcs                     # git status" in ~/.p10k.zsh
# fi
# echo ""

# use the function to change the lines
# change_line "    # os_icon               # os identifier" "    os_icon                 # os identifier" ~/.p10k.zsh
# change_line "    dir                     # current directory" "    # dir                   # current directory" ~/.p10k.zsh

# line=$1
# file=$2
# line_above=$3
# line_below=$4
# is_commented=false
# comment="#* MODIFIED"

# add_line -a "  Lewi needs a new custom line below it" "THIS IS A LINE ABOVE" ~/.p10k.zsh

# unction: test_function "new_line" --above "new_line" in "file"
# test_function "This is a line above" -a "  Lewi needs a new custom line below it" ~/.p10k.zsh
# line -h
# line add "  This is a line above" above "  Lewi needs a new custom line above it" in ~/.p10k.zsh
# line add "  This is a line below" below "  Lewi needs a new custom line above it" in ~/.p10k.zsh
# line append " #! MODIFIED" to "  Lewi needs a new custom line above it" in ~/.p10k.zsh
# line remove "  this is a line over" from ~/.p10k.zsh
# line add " This is at the end of the file" at end of ~/.p10k.zsh
# line change "    # os_icon               # os identifier" to "    os_icon                 # os identifier" in ~/.p10k.zsh
# line change "    dir                     # current directory" to "    # dir                   # current directory" in ~/.p10k.zsh
