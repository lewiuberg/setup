"""Section screen — per-item checklist + run action.

Reads the section's TOML (if any), pre-ticks per `default` flag, lets the
user toggle items with Space, then runs only the ticked ones on Enter.

For sections without a config_file (Rosetta, Homebrew, etc.) the screen
shows a one-line description and runs the section directly on Enter.
"""

from __future__ import annotations

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Static

from macsetup.core.config import Item, load_items
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.sudo import is_cached as sudo_cached
from macsetup.screens.progress import ProgressScreen
from macsetup.screens.sudo_modal import SudoModal
from macsetup.sections.base import Section


CHECK_ON = "[#6a9955]☒[/]"
CHECK_OFF = "[#6a9955]☐[/]"


class SectionScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("space", "toggle", "Toggle"),
        Binding("a", "tick_all", "Tick all"),
        Binding("n", "untick_all", "Untick all"),
        Binding("enter", "run", "Run ticked"),
    ]

    def __init__(self, section: Section) -> None:
        super().__init__()
        self.section = section
        self.items: list[Item] = []
        self.ticked: list[bool] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(
            f"[bold]{self.section.name}[/] — {self.section.description}",
            id="section-title",
        )
        if self.section.config_file:
            try:
                self.items = load_items(CONFIG_DIR / self.section.config_file)
                self.ticked = [item.default for item in self.items]
            except Exception as e:
                yield Static(f"[#f44747]Failed to load config: {e}[/]")
                yield Footer()
                return

            table = DataTable(id="items", cursor_type="row", zebra_stripes=True)
            table.add_columns("✓", "Name", "Description")
            for item, tick in zip(self.items, self.ticked):
                table.add_row(
                    CHECK_ON if tick else CHECK_OFF,
                    item.name,
                    item.description or "",
                )
            yield table
        else:
            yield Static("[i]No item list — press Enter to run this section.[/]")
        yield Footer()

    # --- Actions -------------------------------------------------------------

    def action_toggle(self) -> None:
        if not self.items:
            return
        table = self.query_one("#items", DataTable)
        row = table.cursor_row
        self.ticked[row] = not self.ticked[row]
        table.update_cell_at(
            (row, 0), CHECK_ON if self.ticked[row] else CHECK_OFF
        )

    def action_tick_all(self) -> None:
        self._set_all(True)

    def action_untick_all(self) -> None:
        self._set_all(False)

    def _set_all(self, value: bool) -> None:
        if not self.items:
            return
        table = self.query_one("#items", DataTable)
        for i in range(len(self.items)):
            self.ticked[i] = value
            table.update_cell_at((i, 0), CHECK_ON if value else CHECK_OFF)

    @work
    async def action_run(self) -> None:
        # @work runs this in a Textual worker, which is what
        # push_screen_wait requires (Textual 8.x).

        # Decide which items to run.
        if self.section.config_file:
            to_run = [
                item for item, tick in zip(self.items, self.ticked) if tick
            ]
            if not to_run:
                self.notify("Nothing ticked.")
                return
        else:
            to_run = []  # section.install gets an empty list and runs implicit steps

        if self.section.requires_sudo and not await sudo_cached():
            ok = await self.app.push_screen_wait(SudoModal())
            if not ok:
                self.notify("Cancelled.")
                return

        self.app.push_screen(ProgressScreen(self.section, to_run))
