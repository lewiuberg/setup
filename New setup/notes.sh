#!/usr/bin/env zsh

source functions.sh

frame_text "Notes"

read -p "Do you want to see the notes? [Y/n] " -n 1 -r REPLY
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    #h! Notes: Pyenv ##############################################################
    read -p "Do you want to see the Pyenv notes? (Y/n/s) " -n 1 -r REPLY
    if [[ ! $REPLY =~ ^[NnSs]$ ]]; then
        echo "\n"
        frame_text "Pyenv"
        echo "Pyenv usage:
List all available versions of Python:
    pyenv install --list
List all installed versions of Python:
    pyenv versions
Install a specific version of Python:
    pyenv install 3.9.1
Uninstall a specific version of Python:
    pyenv uninstall 3.9.1
Set a global version of Python:
    pyenv global 3.9.1
Set a local version of Python:
    pyenv local 3.9.1
Set a shell version of Python:
    pyenv shell 3.9.1
"
    elif [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Aborting all notes"
        exit 0
    else
        echo "\nSkipping Pyenv notes\n"
    fi
    #h! Notes: Zsh Autoswitch #####################################################
    read -p "Do you want to see the Zsh Autoswitch notes? (Y/n/s) " -n 1 -r REPLY
    if [[ ! $REPLY =~ ^[NnSs]$ ]]; then
        echo "\n"
        frame_text "Zsh Autoswitch"
        echo "Zsh Autoswitch usage:"
    elif [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Aborting all notes"
        exit 0
    else
        echo "\nSkipping Zsh Autoswitch notes\n"
    fi
    #h! Notes: Poetry #############################################################
    read -p "Do you want to see the Poetry notes? (Y/n/s) " -n 1 -r REPLY
    if [[ ! $REPLY =~ ^[NnSs]$ ]]; then
        echo "\n"
        frame_text "Poetry"
        echo "Poetry usage:
To install dependencies:
    poetry install
"
    elif [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Aborting all notes"
        exit 0
    else
        echo "\nSkipping Poetry notes\n"
    fi
    echo "\nDone"
else
    echo "Skipping notes"
fi
