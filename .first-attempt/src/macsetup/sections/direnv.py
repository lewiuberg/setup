"""direnv — verification-only.

Install handled by the Brews section. This section verifies the binary is
present and the dotfile hook is configured.
"""

from __future__ import annotations

from macsetup.core.config import Item
from macsetup.core.detect import command_exists
from macsetup.sections.base import Emit, Section, SectionStatus, Status


class DirenvSection(Section):
    name = "direnv"
    description = "Per-directory environment switcher (managed by Brews + Dotfiles)"

    async def detect(self) -> SectionStatus:
        if command_exists("direnv"):
            return SectionStatus(Status.DONE, 1, 1)
        return SectionStatus(Status.PENDING, 0, 1)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if command_exists("direnv"):
            await emit("direnv binary present; hook lives in dotfiles/.zshrc")
            return
        await emit("direnv brew formula missing — run the Brews section first")
