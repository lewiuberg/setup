#!/usr/bin/env zsh

# Install oh my zsh
curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh

# Install Powerlevel10k
brew install romkatv/powerlevel10k/powerlevel10k
echo 'source /usr/local/opt/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc

# Install nerd fonts
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font
brew install --cask font-space-mono

# Install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install zsh-autoswitch-virtualenv
git clone "https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv.git" "$ZSH_CUSTOM/plugins/autoswitch_virtualenv"

# Update .zshrc to activate autoswitch-virtualenv
sed -i '' 's/# Add wisely, as too many plugins slow down shell startup./# Add wisely, as too many plugins slow down shell startup.\nplugins=(brew git gh poetry wd vscode docker zsh-autosuggestions zsh-syntax-highlighting)\n# plugins not in use: direnv docker-compose docker-machine/n/nplugins=(autoswitch_virtualenv $plugins)/n/g' ~/.zshrc

# Append zshrc with custom settings.
printf '%s\n' "" \
    "" \
    "################################################################################" \
    "# CUSTOM BY USER" \
    "################################################################################" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Aliases" \
    "# ------------------------------------------------------------------------------" \
    "alias lss='ls -alhS'" \
    "alias lsla='ls -la'" \
    "alias ch='history | grep \"git commit\"'" \
    "alias pih='history | grep \"pip install\"'" \
    "alias hg='history | grep'" \
    "alias ppip=\"python3 -m pip\"" \
    "" \
    "# Show/hide hidden files in Finder" \
    "alias show=\"defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder\"" \
    "alias hide=\"defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder\"" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Powerlevel 10k" \
    "# ------------------------------------------------------------------------------" \
    "source /usr/local/opt/powerlevel10k/powerlevel10k.zsh-theme" \
    "" \
    "# To customize prompt, run 'p10k configure' or edit ~/.p10k.zsh." \
    "[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh" \
    "export PATH=\"/usr/local/sbin:\$PATH\"" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Ruby" \
    "# ------------------------------------------------------------------------------" \
    "export PATH=\"/usr/local/opt/ruby/bin:\$PATH\"" \
    "export PATH=\"\$HOME/.gem/ruby/2.7.0/bin:\$PATH\"" \
    "export PATH=~/.gem/ruby/3.0.0/bin:\$PATH" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# PYENV" \
    "# ------------------------------------------------------------------------------" \
    "#export PATH=\"\$HOME/.pyenv/bin:\$PATH\"" \
    "#eval \"\$(pyenv init -)\"" \
    "#eval \"\$(pyenv virtualenv-init -)\"" \
    "" \
    "if command -v pyenv 1>/dev/null 2>&1; then" \
    "  eval \"\$(pyenv init -)\"" \
    "fi" \
    "" \
    "if which pyenv-virtualenv-init > /dev/null; then" \
    "  eval \"\$(pyenv virtualenv-init -)\";" \
    "fi" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# tcl-tk" \
    "# ------------------------------------------------------------------------------" \
    "export PATH=\"/usr/local/opt/tcl-tk/bin:\$PATH\"" \
    "export LDFLAGS=\"-L/usr/local/opt/tcl-tk/lib\"" \
    "export CPPFLAGS=\"-I/usr/local/opt/tcl-tk/include\"" \
    "export PKG_CONFIG_PATH=\"/usr/local/opt/tcl-tk/lib/pkgconfig\"" \
    "export PYTHON_CONFIGURE_OPTS=\"--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6'\"" \
    "" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Homebrew" \
    "# ------------------------------------------------------------------------------" \
    "# export PATH=\"/usr/local/opt/openssl@1.1/bin:\$PATH\"" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Direnv" \
    "# ------------------------------------------------------------------------------" \
    "eval \"\$(direnv hook zsh)\"" \
    "export EDITOR="code --wait"" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# Poetry" \
    "# ------------------------------------------------------------------------------" \
    "fpath+=~/.zfunc" \
    "" \
    "# ------------------------------------------------------------------------------" \
    "# New" \
    "# ------------------------------------------------------------------------------" \
    "" \
    >>~/.zshrc

# Setup for pyenv
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
