#!/usr/bin/env zsh

source functions.sh
source constants.sh

# Homebrew: Install ###########################################################
sleep 1
frame_text "Homebrew"

if [ -d "/opt/homebrew" ] || [ -d "/usr/local" ]; then
    echo "Homebrew is already installed"
else
    echo "Installing Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew doctor
    brew update
fi

ZPROFILE_HOMEBREW='# ------------------------------------------------------------------------------
# Homebrew
# ------------------------------------------------------------------------------
# Set PATH, MANPATH, etc., for Homebrew.'
if [ "$ARCH_ARM64" = true ]; then
    ZPROFILE_HOMEBREW="$ZPROFILE_HOMEBREW
eval \"\$(/opt/homebrew/bin/brew shellenv)\""
elif [ "$ARCH_86_64" = true ]; then
    ZPROFILE_HOMEBREW="$ZPROFILE_HOMEBREW
eval \"\$(/usr/local/bin/brew shellenv)\""
fi

# check if ZPROFILE_HOMEBREW is in .zprofile
if [[ "$(cat ~/.zprofile)" != *"$ZPROFILE_HOMEBREW"* ]]; then
    echo "Appending Homebrew settings for arm64"
    # check if file is empty
    if [ -s ~/.zprofile ]; then
        # check if last line is empty, if not, add an empty line
        if [ "$(tail -c 1 ~/.zprofile)" != "" ]; then
            echo "\n" >>~/.zprofile
        else
            echo "" >>~/.zprofile
        fi
    fi
    echo "$ZPROFILE_HOMEBREW" >>~/.zprofile
else
    echo "Homebrew settings already in .zprofile"
fi

# source shell
if [ "$ARCH_ARM64" = true ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    echo "Sourced shell for arm64"
elif [ "$ARCH_86_64" = true ]; then
    eval "$(/usr/local/bin/brew shellenv)"
    echo "Sourced shell for x86_64/i386"
fi

echo ""

# Homebrew: Install Packages ##################################################
# Read brew_formulas.sh to get all packages, casks, and taps
brew_taps=$(grep -E "^\s*brew tap" brew_formulas.sh | sed -e "s/brew tap //g" | sed -e "s/#.*//g" | sed -e "s/ && brew install.*//g")
brew_formulas=$(grep -E "^\s*brew install | && brew install" brew_formulas.sh | grep -vE "^\s*#" | sed -e "s/#.*//g" | sed -e "s/.*&& brew install //g" | sed -e "s/brew install //g")
# Separate brew packages and brew casks
brew_packages=$(echo "$brew_formulas" | grep -vF -- "--cask")
brew_casks=$(echo "$brew_formulas" | grep -F -- "--cask" | sed -e "s/--cask //g")

# get installed packages, casks, and taps
brew_taps_installed=$(brew tap)
brew_packages_installed=$(brew list --formula)
brew_casks_installed=$(brew list --cask)

# remove all taps that are already installed
brew_taps=$(echo "$brew_taps" | grep -vF "$brew_taps_installed")

# remove all packages that are already installed
brew_packages=$(echo "$brew_packages" | grep -vF "$brew_packages_installed")

# remove all casks that are already installed
brew_casks=$(echo "$brew_casks" | grep -vF "$brew_casks_installed")

# Homebrew: Tap Repositories ##################################################
sleep 1
frame_text "Homebrew: Tap Repositories"

# if brew_taps is not empty
if [ -n "$brew_taps" ]; then
    for brew_tap in $brew_taps; do
        echo "Tapping $brew_tap"
        #! brew tap $brew_tap
        echo "brew tap $brew_tap"
        echo "Repository tapped"
        echo ""
    done
    echo "Finished tapping repositories"
else
    echo "All repositories already tapped"
fi
echo ""

# Homebrew: Install Packages ##################################################
sleep 1
frame_text "Homebrew: Install Packages"

# if brew_packages is not empty
if [ -n "$brew_packages" ]; then
    for brew_package in $brew_packages; do
        echo "Installing package: $brew_package"
        #! brew install $brew_package
        echo "brew install $brew_package"
        echo "Package installed"
        echo ""
    done
    echo "Finished installing packages"
else
    echo "All Homebrew packages are already installed"
fi
echo ""

# Homebrew: Install Casks ####################################################
sleep 1
frame_text "Homebrew: Install Casks"

# if brew_casks is not empty
if [ -n "$brew_casks" ]; then
    for brew_cask in $brew_casks; do
        echo "Installing cask: $brew_cask"
        #! brew install --cask $brew_cask
        echo "brew install --cask $brew_cask"
        echo "Cask installed"
        echo ""
    done
    echo "Finished installing casks"
else
    echo "All Homebrew casks are already installed"
fi
echo ""

# Homebrew: Cleanup ##########################################################
sleep 1
frame_text "Homebrew: Cleanup"

echo "Cleaning up Homebrew"
#! brew cleanup
echo "Finished cleaning up Homebrew"

echo ""
