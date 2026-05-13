"""Homebrew taps — extra formula repositories."""

from __future__ import annotations

from macsetup.core.config import Item, load_items
from macsetup.core.detect import installed_taps
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


class TapsSection(Section):
    name = "Taps"
    description = "Extra Homebrew taps"
    config_file = "taps.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        installed = await installed_taps()
        count = sum(1 for item in items if item.name in installed)
        total = len(items)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0, "No taps configured")
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if count == total:
            return SectionStatus(Status.DONE, count, total)
        return SectionStatus(Status.PARTIAL, count, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        installed = await installed_taps()
        for item in items:
            if item.name in installed:
                await emit(f"already tapped: {item.name}")
                continue
            await emit(f"brew tap {item.name}")
            result = await run(["brew", "tap", item.name], on_line=emit)
            if not result.ok:
                await emit(f"failed: {item.name}: {result.stderr.strip()}")
