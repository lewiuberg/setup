"""Homebrew installation.

The official Homebrew installer handles the architecture detection and PATH
nudging itself; we just run it. The .zprofile dotfile (Phase 5) takes care
of re-sourcing brew shellenv on subsequent shell launches.
"""

from __future__ import annotations

from macsetup.core.arch import brew_bin
from macsetup.core.config import Item
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


INSTALL_URL = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"


class HomebrewSection(Section):
    name = "Homebrew"
    description = "The missing package manager for macOS"
    requires_sudo = True  # the installer asks for sudo internally

    async def detect(self) -> SectionStatus:
        if brew_bin().exists():
            return SectionStatus(Status.DONE, 1, 1)
        return SectionStatus(Status.PENDING, 0, 1)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if brew_bin().exists():
            await emit(f"Homebrew already installed at {brew_bin()}")
            return
        await emit("Installing Homebrew…")
        result = await run(
            ["bash", "-c", f"curl -fsSL {INSTALL_URL} | bash"],
            on_line=emit,
        )
        if result.ok:
            await emit("Homebrew installed")
        else:
            await emit(f"Homebrew install failed: {result.stderr.strip()}")
