"""Ordered registry of installable sections.

Order = display order on the Home screen. To add a new section: create
sections/<name>.py implementing Section, import it here, and add it to
SECTIONS at the position you want.

To disable a section without deleting it, comment out its entry below.
"""

from macsetup.sections.app_store import AppStoreSection
from macsetup.sections.base import Section
from macsetup.sections.brews import BrewsSection
from macsetup.sections.casks import CasksSection
from macsetup.sections.direnv import DirenvSection
from macsetup.sections.dotfiles import DotfilesSection
from macsetup.sections.dotnet import DotnetSection
from macsetup.sections.fonts import FontsSection
from macsetup.sections.homebrew import HomebrewSection
from macsetup.sections.oh_my_zsh import OhMyZshSection
from macsetup.sections.powerlevel10k import Powerlevel10kSection
from macsetup.sections.pyenv import PyenvSection
from macsetup.sections.python_tools import PythonToolsSection
from macsetup.sections.raycast import RaycastSection
from macsetup.sections.rosetta import RosettaSection
from macsetup.sections.secrets import SecretsSection
from macsetup.sections.taps import TapsSection
from macsetup.sections.terminal_profile import TerminalProfileSection
from macsetup.sections.vscode import VSCodeSection
from macsetup.sections.zsh_plugins import ZshPluginsSection


SECTIONS: list[Section] = [
    RosettaSection(),
    HomebrewSection(),
    TapsSection(),
    BrewsSection(),
    CasksSection(),
    FontsSection(),
    AppStoreSection(),
    OhMyZshSection(),
    Powerlevel10kSection(),
    PyenvSection(),
    PythonToolsSection(),
    DirenvSection(),
    DotnetSection(),
    ZshPluginsSection(),
    DotfilesSection(),
    VSCodeSection(),
    RaycastSection(),
    SecretsSection(),
    TerminalProfileSection(),
]
