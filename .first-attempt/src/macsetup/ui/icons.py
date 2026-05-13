"""Nerd Font glyphs per section.

Codepoints from the Font Awesome / Devicons ranges bundled in Nerd Fonts.
MesloLG Nerd Font (installed by the Fonts section) renders these.
Without a Nerd Font, terminals show a missing-glyph box — not fatal.
"""

SECTION_ICONS: dict[str, str] = {
    "Rosetta": "",          # Apple logo
    "Homebrew": "",         # beer mug
    "Taps": "",             # tag
    "Brews": "",            # cubes
    "Casks": "",            # box
    "Fonts": "",            # font A
    "App Store": "",        # Apple symbol (PUA — also renders in non-Nerd fonts)
    "Oh My Zsh": "",        # terminal prompt
    "Powerlevel10k": "",    # lightbulb
    "pyenv": "",            # Python
    "Python tools": "",     # Python alt (devicons)
    "direnv": "",           # cog
    ".NET": "",             # Microsoft
    "zsh plugins": "",      # plug
    "Dotfiles": "",         # link
    "VS Code": "",          # VS Code (devicons)
    "Raycast": "",          # rocket
    "Secrets": "",          # key
    "Terminal profile": "", # terminal alt
}


def icon_for(name: str) -> str:
    return SECTION_ICONS.get(name, "")  # default: question circle
