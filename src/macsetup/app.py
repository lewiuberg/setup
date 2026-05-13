from pathlib import Path

from textual.app import App

from macsetup.screens.plan import PlanScreen

THEME_CSS = Path(__file__).parent / "ui" / "dark_plus.tcss"


class MacsetupApp(App):
    """Plan-then-execute wizard for macOS dev-environment setup."""

    CSS_PATH = str(THEME_CSS)
    TITLE = "macsetup"
    SUB_TITLE = "macOS dev-environment wizard"

    def __init__(self, *, dry_run: bool = False) -> None:
        super().__init__()
        self.dry_run = dry_run
        if dry_run:
            self.sub_title = "macOS dev-environment wizard (dry-run)"

    def on_mount(self) -> None:
        self.push_screen(PlanScreen(dry_run=self.dry_run))
