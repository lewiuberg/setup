"""Raycast cask + extension browser hand-off.

Free-tier Raycast has no programmatic extension install. The section
installs the cask, opens Raycast (so the `raycast://` URL scheme is
registered), then opens each ticked Store URL in the browser — clicking
"Install Extension" on the Store page completes the install in Raycast
(one Return press).
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from macsetup.core.config import Item, load_items
from macsetup.core.detect import installed_casks
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


RAYCAST_APP = Path("/Applications/Raycast.app")
# Open delay between URLs so the browser doesn't race with itself.
OPEN_DELAY_SECONDS = 1.5


class RaycastSection(Section):
    name = "Raycast"
    description = "Productivity launcher (free tier — browser hand-off for extensions)"
    config_file = "raycast_extensions.toml"

    async def detect(self) -> SectionStatus:
        # We can reliably detect the app, but not individual extensions
        # (folder structure under com.raycast.macos is opaque). Status counts
        # the app + a single proxy "extensions" check (always 0 unless app installed).
        app_installed = RAYCAST_APP.exists() or "raycast" in await installed_casks()
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        total = 1 + len(items)
        installed = 1 if app_installed else 0
        # Individual extensions can't be confirmed; report partial when app is up.
        if not app_installed:
            return SectionStatus(Status.PENDING, 0, total, "Raycast app not installed")
        return SectionStatus(
            Status.PARTIAL, installed, total,
            "Raycast app installed — extensions require manual click-through",
        )

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not RAYCAST_APP.exists() and "raycast" not in await installed_casks():
            await emit("Installing Raycast cask…")
            result = await run(
                ["brew", "install", "--cask", "raycast"], on_line=emit
            )
            if not result.ok:
                await emit(f"Raycast install failed: {result.stderr.strip()}")
                return
        await emit("Opening Raycast (one-time launch to register URL scheme)…")
        await run(["open", "-a", "Raycast"], on_line=emit)

        if not items:
            await emit("No extensions ticked — done")
            return

        await emit("")
        await emit(
            "For each tab that opens: click 'Install Extension' on the Store "
            "page. Raycast will take focus — press Return to confirm install."
        )
        await emit("")

        for item in items:
            url = item.extras.get("url")
            if not url:
                await emit(f"skipping {item.name}: missing `url` in TOML")
                continue
            await emit(f"open {url}")
            await run(["open", str(url)], on_line=emit)
            await asyncio.sleep(OPEN_DELAY_SECONDS)
