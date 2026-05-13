"""Home screen — single-column section list with live status."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static

from macsetup.screens.section import SectionScreen
from macsetup.sections import SECTIONS
from macsetup.ui.icons import icon_for
from macsetup.ui.widgets import render_row


class HomeScreen(Screen):
    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("w", "wizard", "Wizard"),
        Binding("question_mark", "help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield ListView(
            *[
                ListItem(
                    Static(f"  •  {section.name}", markup=True),
                    id=f"section-{i}",
                    name=section.name,
                )
                for i, section in enumerate(SECTIONS)
            ],
            id="home-sections",
        )
        yield Footer()

    async def on_mount(self) -> None:
        await self._refresh_all()

    async def _refresh_all(self) -> None:
        list_view = self.query_one("#home-sections", ListView)
        for i, section in enumerate(SECTIONS):
            try:
                status = await section.detect()
            except Exception as e:
                rendered = f"  ?  [bold]{section.name:<22}[/]  [#f44747]error: {e}[/]"
            else:
                rendered = render_row(icon_for(section.name), section.name, status)
            item = list_view.get_child_by_id(f"section-{i}")
            assert isinstance(item, ListItem)
            static = item.query_one(Static)
            static.update(rendered)

    async def action_refresh(self) -> None:
        self.notify("Re-detecting all sections…", timeout=1)
        await self._refresh_all()

    def action_help(self) -> None:
        self.notify("arrows + Enter open · r refresh · w wizard · Ctrl+Q quit")

    def action_wizard(self) -> None:
        from macsetup.screens.wizard import WizardScreen
        self.app.push_screen(WizardScreen())

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # ListView consumes Enter and fires this event; we route to the
        # SectionScreen for whichever item is highlighted.
        list_view = self.query_one("#home-sections", ListView)
        if list_view.index is None:
            return
        section = SECTIONS[list_view.index]
        self.app.push_screen(SectionScreen(section))

    async def on_screen_resume(self) -> None:
        # Returning from SectionScreen or ProgressScreen → re-detect.
        await self._refresh_all()
