"""One-time sudo password prompt.

Modal screen. The password is held only as a local string for the
lifetime of the validate() call; never written to disk or environment.
On successful validation, the app's background keep-alive task begins.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Static

from macsetup.core.sudo import SudoError, validate


class SudoModal(ModalScreen[bool]):
    """Returns True iff sudo was validated successfully."""

    BINDINGS = [Binding("escape", "dismiss(False)", "Cancel")]

    DEFAULT_CSS = """
    SudoModal {
        align: center middle;
    }
    SudoModal > Vertical {
        background: #1e1e1e;
        border: tall #007acc;
        padding: 1 2;
        width: 60;
        height: auto;
    }
    SudoModal Label.title {
        content-align: center middle;
        color: #d4d4d4;
        margin-bottom: 1;
    }
    SudoModal Static.error {
        color: #f44747;
        margin-top: 1;
    }
    SudoModal Input {
        background: #1e1e1e;
        border: tall #264f78;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("[bold]Sudo password[/]", classes="title")
            yield Label("Needed once for this session.")
            yield Input(password=True, id="password")
            yield Static("", id="error", classes="error")

    def on_mount(self) -> None:
        self.query_one("#password", Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        password = event.value
        error = self.query_one("#error", Static)
        try:
            await validate(password)
        except SudoError as e:
            error.update(f"✗ {e}")
            event.input.value = ""
            event.input.focus()
            return
        # Start background keep-alive so subsequent sections don't re-prompt.
        await self.app.ensure_sudo_keepalive()  # type: ignore[attr-defined]
        self.dismiss(True)
