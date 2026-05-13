"""Capture SVG screenshots of every key screen.

Run from the repo root:
    uv run python scripts/capture_screenshots.py

Writes to assets/screenshots/*.svg. Safe to re-run on every UI change so
the README's embedded images don't go stale.

Note: SVG screenshots use a fallback monospace font for the embedded text;
Nerd Font glyphs render as missing-glyph boxes in the SVG even though
they display correctly in a real terminal. The Brews/Casks/etc. row
content (progress bars, fractions, colours) all render faithfully.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from macsetup.app import MacSetupApp
from macsetup.screens.progress import ProgressScreen
from macsetup.screens.section import SectionScreen
from macsetup.screens.sudo_modal import SudoModal
from macsetup.sections import SECTIONS


OUT = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
SIZE = (120, 36)


async def shoot_home(app: MacSetupApp) -> None:
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause(1.0)
        app.save_screenshot(str(OUT / "home.svg"))


async def shoot_section() -> None:
    """Open the Brews section so the checklist is on screen."""
    app = MacSetupApp()
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause(1.0)
        # Move cursor down to the Brews row (index 3) and open it.
        for _ in range(3):
            await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause(0.5)
        app.save_screenshot(str(OUT / "section.svg"))


async def shoot_progress() -> None:
    """Push ProgressScreen directly with a fake section so the log is populated."""
    from macsetup.core.config import Item
    from macsetup.sections.base import Emit, Section, SectionStatus, Status

    class DemoSection(Section):
        name = "Brews (demo)"
        description = "Demo run for screenshot"

        async def detect(self) -> SectionStatus:
            return SectionStatus(Status.PENDING, 0, 3)

        async def install(self, items: list[Item], emit: Emit) -> None:
            await emit("[#007acc]▶ Starting Brews (demo)…[/]")
            await emit("brew install git")
            await emit("git is already installed")
            await emit("brew install gh")
            await emit("✓ gh installed")
            await emit("brew install tmux")
            await emit("✓ tmux installed")
            await emit("")
            await emit("[#6a9955]✓ Section finished. Press Esc to return.[/]")

    app = MacSetupApp()
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause(0.3)
        app.push_screen(ProgressScreen(DemoSection(), []))
        await pilot.pause(0.6)
        app.save_screenshot(str(OUT / "progress.svg"))


async def shoot_sudo() -> None:
    app = MacSetupApp()
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause(0.3)
        app.push_screen(SudoModal())
        await pilot.pause(0.3)
        app.save_screenshot(str(OUT / "sudo.svg"))


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    await shoot_home(MacSetupApp())
    print(f"saved {OUT / 'home.svg'}")
    await shoot_section()
    print(f"saved {OUT / 'section.svg'}")
    await shoot_progress()
    print(f"saved {OUT / 'progress.svg'}")
    await shoot_sudo()
    print(f"saved {OUT / 'sudo.svg'}")


if __name__ == "__main__":
    asyncio.run(main())
