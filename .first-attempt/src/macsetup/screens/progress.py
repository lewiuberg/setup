"""Progress screen — live log of a section's install run.

Runs section.install(items, emit) where emit appends to a RichLog.
Esc returns to the previous screen. Subprocess output is streamed
line-by-line; the screen never blocks the UI.
"""

from __future__ import annotations

import asyncio

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, RichLog, Static

from macsetup.core.config import Item
from macsetup.sections.base import Section


class ProgressScreen(Screen):
    BINDINGS = [
        Binding("escape", "dismiss_progress", "Back"),
    ]

    def action_dismiss_progress(self) -> None:
        # Use dismiss() so callers using push_screen_wait (the Wizard) get
        # control back; for callers that used push_screen (SectionScreen)
        # dismiss is equivalent to pop_screen.
        self.dismiss(None)

    def __init__(self, section: Section, items: list[Item]) -> None:
        super().__init__()
        self.section = section
        self.items = items
        self._task: asyncio.Task[None] | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(
            f"[bold]{self.section.name}[/] — running [#dcdcaa]{len(self.items)}[/] item(s)",
            id="progress-title",
        )
        yield RichLog(highlight=True, markup=True, wrap=False, id="log")
        yield Footer()

    async def on_mount(self) -> None:
        log = self.query_one("#log", RichLog)

        async def emit(line: str) -> None:
            log.write(line)

        async def runner() -> None:
            await emit(f"[#007acc]▶ Starting {self.section.name}…[/]")
            try:
                await self.section.install(self.items, emit)
                await emit("")
                await emit("[#6a9955]✓ Section finished. Press Esc to return.[/]")
            except Exception as e:
                await emit(f"[#f44747]✗ Section failed: {e}[/]")

        self._task = asyncio.create_task(runner())

    async def on_unmount(self) -> None:
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
