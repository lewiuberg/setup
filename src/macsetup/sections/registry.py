from __future__ import annotations

from macsetup.sections.base import Section

ALL_SECTIONS: list[Section] = [
    Section(
        "rosetta",
        "Rosetta 2",
        "Apple Silicon shim for running Intel binaries. No-op on x86_64 Macs.",
    ),
    Section(
        "homebrew",
        "Homebrew",
        "Install Homebrew if missing, then run `brew doctor` and `brew update`.",
    ),
    Section(
        "taps",
        "Homebrew taps",
        "Additional Homebrew repositories.",
        items_config="taps",
    ),
    Section(
        "brews",
        "Brew formulae",
        "Command-line tools installed via `brew install`.",
        items_config="brews",
    ),
    Section(
        "casks",
        "Brew casks",
        "GUI apps installed via `brew install --cask`.",
        items_config="casks",
    ),
    Section(
        "fonts",
        "Fonts",
        "Nerd Fonts and developer fonts (Meslo, Fira, JetBrains, …) via brew cask.",
        items_config="fonts",
    ),
    Section(
        "mas",
        "App Store apps",
        "Apps from the Mac App Store via the `mas` CLI. Requires sign-in.",
        items_config="mas_apps",
    ),
    Section(
        "oh_my_zsh",
        "Oh My Zsh",
        "Zsh framework with themes and plugins. Idempotent install.",
    ),
    Section(
        "zsh_plugins",
        "Zsh plugins",
        "zsh-syntax-highlighting and zsh-autosuggestions.",
    ),
    Section(
        "dotfiles",
        "Dotfiles",
        "Generate ~/.zshrc, ~/.zprofile, ~/.warprc. Existing files backed up to ~/.dotfile-backups/<timestamp>/.",
    ),
    Section(
        "powerlevel10k",
        "Powerlevel10k",
        "Clone the theme, then pause so you can open a new terminal and run the configurator.",
        interactive=True,
    ),
    Section(
        "mise",
        "mise + runtimes",
        "Polyglot version manager (replaces pyenv + asdf). Installs the runtimes you tick.",
        items_config="mise_runtimes",
    ),
    Section(
        "python_tools",
        "Python tools",
        "uv (recommended) and Poetry (opt-in, with 2.x-aware config fix).",
    ),
    Section(
        "raycast",
        "Raycast + extensions",
        "Launcher app and curated extensions (opened in the Store one by one).",
        items_config="raycast_extensions",
    ),
    Section(
        "manual_apps",
        "Manual app installs",
        "Apps that aren't on the App Store or in Homebrew. Opens download URLs.",
        items_config="manual_apps",
    ),
    Section(
        "vscode",
        "VS Code extensions",
        "Opens VS Code so Settings Sync can run, then tops up any missing baseline extensions.",
        items_config="vscode_extensions",
        interactive=True,
    ),
    Section(
        "github_auth",
        "GitHub auth",
        "Run `gh auth login` — generates SSH key, uploads to GitHub, configures credential helper and signing.",
        interactive=True,
    ),
    Section(
        "azure_devops",
        "Azure DevOps auth",
        "Copies your SSH public key to clipboard and opens the Azure DevOps SSH keys page.",
        interactive=True,
    ),
    Section(
        "html_guide",
        "Usage guide",
        "Generate ~/MACSETUP-USAGE.html templated by what you installed, then open it.",
    ),
]

SECTIONS_BY_SLUG: dict[str, Section] = {s.slug: s for s in ALL_SECTIONS}
