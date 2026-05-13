"""First-run wizard — walks through every section in order.

Same checklist UI as SectionScreen, but with wizard-specific footer:
  Space  toggle item
  a      tick all
  n      untick all
  r      Run this section (then auto-advance)
  s      Skip this section (advance without running)
  b      Back to previous section
  Esc    Quit wizard (drop to dashboard)

After the last section, writes a marker file (~/.local/state/macsetup/
first-run-complete) so subsequent launches go straight to the dashboard.
"""

from __future__ import annotations

from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from macsetup.core.config import Item, load_items
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.sudo import is_cached as sudo_cached
from macsetup.screens.progress import ProgressScreen
from macsetup.screens.sudo_modal import SudoModal
from macsetup.sections import SECTIONS


FIRST_RUN_MARKER = Path("~/.local/state/macsetup/first-run-complete").expanduser()

CHECK_ON = "[#6a9955]☒[/]"
CHECK_OFF = "[#6a9955]☐[/]"


def mark_first_run_complete() -> None:
    FIRST_RUN_MARKER.parent.mkdir(parents=True, exist_ok=True)
    FIRST_RUN_MARKER.touch()


def first_run_done() -> bool:
    return FIRST_RUN_MARKER.exists()


class WizardScreen(Screen):
    BINDINGS = [
        Binding("space", "toggle", "Toggle item"),
        Binding("a", "tick_all", "Tick all"),
        Binding("n", "untick_all", "Untick all"),
        Binding("r", "run_section", "Run"),
        Binding("s", "skip_section", "Skip"),
        Binding("b", "previous_section", "Back"),
        Binding("escape", "quit_wizard", "Quit wizard"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.index = 0
        self.items: list[Item] = []
        self.ticked: list[bool] = []
        self.ran: list[int] = []      # section indexes the user ran
        self.skipped: list[int] = []  # section indexes the user skipped

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static("", id="wizard-title")
        yield Static("", id="wizard-description")
        yield DataTable(id="items", cursor_type="row", zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        self._show_section()

    def _show_section(self) -> None:
        section = SECTIONS[self.index]
        self.query_one("#wizard-title", Static).update(
            f"[bold]Step {self.index + 1}/{len(SECTIONS)}[/]  —  "
            f"[bold #007acc]{section.name}[/]"
        )
        self.query_one("#wizard-description", Static).update(
            f"[#d4d4d4]{section.description}[/]"
        )
        table = self.query_one("#items", DataTable)
        table.clear(columns=True)
        if section.config_file:
            try:
                self.items = load_items(CONFIG_DIR / section.config_file)
                self.ticked = [item.default for item in self.items]
            except Exception as e:
                table.add_columns("status")
                table.add_row(f"Failed to load config: {e}")
                self.items = []
                self.ticked = []
                return
            table.add_columns("✓", "Name", "Description")
            for item, tick in zip(self.items, self.ticked):
                table.add_row(
                    CHECK_ON if tick else CHECK_OFF,
                    item.name,
                    item.description or "",
                )
        else:
            self.items = []
            self.ticked = []
            table.add_columns("info")
            table.add_row("No item list — press [r] to run this section, [s] to skip.")

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
    async def action_run_section(self) -> None:
        # @work runs this in a Textual worker — required by push_screen_wait
        # in Textual 8.x.
        section = SECTIONS[self.index]
        to_run = (
            [item for item, tick in zip(self.items, self.ticked) if tick]
            if section.config_file
            else []
        )
        if section.config_file and not to_run:
            self.notify("Nothing ticked. Press 's' to skip or tick at least one item.")
            return
        if section.requires_sudo and not await sudo_cached():
            ok = await self.app.push_screen_wait(SudoModal())
            if not ok:
                self.notify("Sudo cancelled — section not run.")
                return
        await self.app.push_screen_wait(ProgressScreen(section, to_run))
        self.ran.append(self.index)
        self._advance()

    def action_skip_section(self) -> None:
        self.skipped.append(self.index)
        self._advance()

    def action_previous_section(self) -> None:
        if self.index == 0:
            self.notify("Already at the first section.")
            return
        self.index -= 1
        # Drop the previous step from ran/skipped if it was just recorded.
        if self.ran and self.ran[-1] == self.index:
            self.ran.pop()
        if self.skipped and self.skipped[-1] == self.index:
            self.skipped.pop()
        self._show_section()

    def action_quit_wizard(self) -> None:
        # User exits without finishing — don't mark first-run-done. They can
        # press `w` on Home to relaunch the wizard.
        from macsetup.screens.home import HomeScreen
        self.app.switch_screen(HomeScreen())

    def _advance(self) -> None:
        if self.index + 1 < len(SECTIONS):
            self.index += 1
            self._show_section()
        else:
            self._show_completion()

    def _show_completion(self) -> None:
        mark_first_run_complete()
        title = self.query_one("#wizard-title", Static)
        desc = self.query_one("#wizard-description", Static)
        table = self.query_one("#items", DataTable)
        title.update("[bold #6a9955]✓ Wizard complete[/]")
        desc.update(
            f"[#d4d4d4]Ran {len(self.ran)} section(s), skipped "
            f"{len(self.skipped)}. Press Esc to open the dashboard.[/]"
        )
        table.clear(columns=True)
        table.add_columns("Step", "Section", "Result")
        for i, section in enumerate(SECTIONS):
            if i in self.ran:
                result = "[#6a9955]ran[/]"
            elif i in self.skipped:
                result = "[#dcdcaa]skipped[/]"
            else:
                result = "[#6a9955]—[/]"
            table.add_row(str(i + 1), section.name, result)
        # Override quit-wizard so it just drops to dashboard.
        # (Same action already does that, so no change needed.)
