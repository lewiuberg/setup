"""Oh My Zsh — community zsh configuration framework."""

from __future__ import annotations

from pathlib import Path

from macsetup.core.config import Item
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


OMZ_DIR = Path.home() / ".oh-my-zsh"
INSTALL_URL = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"


class OhMyZshSection(Section):
    name = "Oh My Zsh"
    description = "Community-driven zsh framework"

    async def detect(self) -> SectionStatus:
        if OMZ_DIR.exists():
            return SectionStatus(Status.DONE, 1, 1)
        return SectionStatus(Status.PENDING, 0, 1)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if OMZ_DIR.exists():
            await emit(f"Oh My Zsh already installed at {OMZ_DIR}")
            return
        await emit("Installing Oh My Zsh (unattended)…")
        # --unattended: don't change shell or run zsh at the end.
        result = await run(
            ["bash", "-c", f'sh -c "$(curl -fsSL {INSTALL_URL})" "" --unattended'],
            on_line=emit,
        )
        if result.ok:
            await emit("Oh My Zsh installed")
        else:
            await emit(f"Oh My Zsh install failed: {result.stderr.strip()}")
