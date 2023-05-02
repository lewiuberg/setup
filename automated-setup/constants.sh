#!/usr/bin/env zsh

USER=$(whoami)

HOMEDIR=$(echo "$HOME" | sed -r -e "s/ /\\\ /g")

ARCH_ARM64=false
ARCH_86_64=false
if [ "$(uname -m)" = "arm64" ]; then
    ARCH_ARM64=true
elif [ "$(uname -m)" = "i386" ] || [ "$(uname -m)" = "x86_64" ]; then
    ARCH_86_64=true
fi
