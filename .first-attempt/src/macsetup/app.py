"""macsetup Textual application.

On launch:
  - If --wizard is set, push WizardScreen.
  - Else if --no-wizard is set, push HomeScreen.
  - Else: if the first-run marker is absent, push WizardScreen; else HomeScreen.

Owns the background sudo keep-alive task that fires once the user
authenticates for the first time.
"""

from __future__ import annotations

import asyncio

from textual.app import App
from textual.binding import Binding

from macsetup.core import sudo
from macsetup.screens.home import HomeScreen
from macsetup.screens.wizard import WizardScreen, first_run_done


class MacSetupApp(App):
    """Interactive macOS setup tool."""

    CSS_PATH = "ui/dark_plus.tcss"
    TITLE = "macsetup"
    SUB_TITLE = "Interactive macOS setup"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
    ]

    _keepalive_task: asyncio.Task[None] | None = None

    def __init__(
        self,
        *,
        force_wizard: bool = False,
        force_dashboard: bool = False,
    ) -> None:
        super().__init__()
        self.force_wizard = force_wizard
        self.force_dashboard = force_dashboard

    def on_mount(self) -> None:
        if self.force_wizard:
            self.push_screen(WizardScreen())
        elif self.force_dashboard:
            self.push_screen(HomeScreen())
        elif not first_run_done():
            self.push_screen(WizardScreen())
        else:
            self.push_screen(HomeScreen())

    async def ensure_sudo_keepalive(self) -> None:
        """Start the background sudo refresh loop if not already running."""
        if self._keepalive_task is not None and not self._keepalive_task.done():
            return

        stop = asyncio.Event()
        self._keepalive_stop = stop

        async def loop() -> None:
            while not stop.is_set():
                try:
                    await asyncio.wait_for(
                        stop.wait(), timeout=sudo.KEEPALIVE_INTERVAL
                    )
                    return
                except asyncio.TimeoutError:
                    from macsetup.core.shell import run
                    await run(["sudo", "-n", "-v"])

        self._keepalive_task = asyncio.create_task(loop())

    async def on_unmount(self) -> None:
        if self._keepalive_task is not None:
            self._keepalive_stop.set()
            self._keepalive_task.cancel()
            try:
                await self._keepalive_task
            except asyncio.CancelledError:
                pass
