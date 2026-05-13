"""Powerlevel10k — verification-only section.

The brew formula install is handled by the Brews section
(brews.toml includes `romkatv/powerlevel10k/powerlevel10k`). The .p10k.zsh
config file is symlinked by the Dotfiles section. This section just
verifies both are in place — no install logic of its own.
"""

from __future__ import annotations

from pathlib import Path

from macsetup.core.config import Item
from macsetup.core.detect import installed_brews
from macsetup.sections.base import Emit, Section, SectionStatus, Status


P10K_CONFIG = Path.home() / ".p10k.zsh"


class Powerlevel10kSection(Section):
    name = "Powerlevel10k"
    description = "Zsh prompt theme — depends on Brews + Dotfiles sections"

    async def _is_brew_installed(self) -> bool:
        return "powerlevel10k" in await installed_brews()

    async def detect(self) -> SectionStatus:
        brew_ok = await self._is_brew_installed()
        cfg_ok = P10K_CONFIG.exists()
        if brew_ok and cfg_ok:
            return SectionStatus(Status.DONE, 2, 2)
        if brew_ok or cfg_ok:
            return SectionStatus(Status.PARTIAL, int(brew_ok) + int(cfg_ok), 2)
        return SectionStatus(Status.PENDING, 0, 2)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not await self._is_brew_installed():
            await emit("powerlevel10k brew formula missing — run the Brews section first")
        if not P10K_CONFIG.exists():
            await emit("~/.p10k.zsh missing — run the Dotfiles section to symlink it")
        if await self._is_brew_installed() and P10K_CONFIG.exists():
            await emit("Powerlevel10k is fully configured")
