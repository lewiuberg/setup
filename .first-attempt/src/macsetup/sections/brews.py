"""Homebrew formulae (CLI tools and libraries)."""

from __future__ import annotations

from macsetup.core.config import Item, load_items
from macsetup.core.detect import installed_brews
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


def _short_name(formula: str) -> str:
    """`smudge/smudge/nightlight` -> `nightlight`. brew list reports the leaf name."""
    return formula.split("/")[-1]


class BrewsSection(Section):
    name = "Brews"
    description = "Homebrew formulae"
    config_file = "brews.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        installed = await installed_brews()
        count = sum(1 for item in items if _short_name(item.name) in installed)
        total = len(items)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if count == total:
            return SectionStatus(Status.DONE, count, total)
        return SectionStatus(Status.PARTIAL, count, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        installed = await installed_brews()
        for item in items:
            if _short_name(item.name) in installed:
                await emit(f"already installed: {item.name}")
                continue
            await emit(f"brew install {item.name}")
            result = await run(["brew", "install", item.name], on_line=emit)
            if not result.ok:
                await emit(f"failed: {item.name}: {result.stderr.strip()}")
