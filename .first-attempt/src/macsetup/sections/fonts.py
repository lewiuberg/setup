"""Font casks. Behaviourally identical to Casks but reads fonts.toml.

Split into its own section so the user can re-run fonts without scanning
the whole cask list, and so the Home screen shows fonts separately.
"""

from __future__ import annotations

from macsetup.core.config import Item, load_items
from macsetup.core.detect import installed_casks
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


class FontsSection(Section):
    name = "Fonts"
    description = "Font casks (Nerd Fonts, programming ligatures)"
    config_file = "fonts.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        installed = await installed_casks()
        count = sum(1 for item in items if item.name in installed)
        total = len(items)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if count == total:
            return SectionStatus(Status.DONE, count, total)
        return SectionStatus(Status.PARTIAL, count, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        installed = await installed_casks()
        for item in items:
            if item.name in installed:
                await emit(f"already installed: {item.name}")
                continue
            await emit(f"brew install --cask {item.name}")
            result = await run(
                ["brew", "install", "--cask", item.name], on_line=emit
            )
            if not result.ok:
                await emit(f"failed: {item.name}: {result.stderr.strip()}")
