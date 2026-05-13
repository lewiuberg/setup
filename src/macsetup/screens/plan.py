from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    ListItem,
    ListView,
    RichLog,
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

from macsetup.core.dryrun import DryRunShell
from macsetup.core.executor import Executor
from macsetup.core.shell import Shell
from macsetup.core.sudo import SudoKeepalive, acquire_sudo
from macsetup.sections.base import Section
from macsetup.sections.registry import ALL_SECTIONS, SECTIONS_BY_SLUG
from macsetup.sections.runners import get_runner
from macsetup.state import PlanState

_STATUS_GLYPHS = {
    "running": ("▶", "#007acc"),
    "ok": ("✓", "#4ec9b0"),
    "failed": ("✗", "#f44747"),
    "skipped": ("·", "#6a737d"),
}


class SectionRow(ListItem):
    """One row in the section list. Shows status (pre-run: enabled/disabled,
    during/after run: running / ok / failed / skipped) plus item count."""

    def __init__(self, section: Section, state: PlanState) -> None:
        self.section = section
        self.state = state
        self._label = Static(self._render_label(), id="row-label")
        super().__init__(self._label, id=f"row-{section.slug}")

    def _render_label(self) -> Text:
        slug = self.section.slug
        status = self.state.section_status.get(slug)
        if status in _STATUS_GLYPHS:
            glyph, glyph_colour = _STATUS_GLYPHS[status]
        else:
            enabled = self.state.is_section_enabled(slug)
            glyph = "✓" if enabled else "·"
            glyph_colour = "#4ec9b0" if enabled else "#6a737d"

        text = Text()
        text.append(glyph, style=glyph_colour)
        text.append(f" {self.section.display_name}")
        if self.section.items_config:
            total = len(self.section.load_items())
            selected = self.state.selected_count(slug)
            text.append(f" ({selected}/{total})", style="#6a737d")
        if self.section.interactive:
            text.append(" ⏵", style="#ce9178")
        return text

    def refresh_row(self) -> None:
        self._label.update(self._render_label())


class PlanScreen(Screen):
    """Two-pane view: section list + right pane that swaps between section
    detail (planning) and a streaming log (running)."""

    CSS_PATH = None  # inherits from app
    BINDINGS = [
        Binding("enter", "toggle_section", "Toggle section", priority=True),
        Binding("right", "focus_detail", "Into section", priority=True),
        Binding("left", "focus_sections", "Back to list", priority=True),
        Binding("a", "select_all_items", "Select all"),
        Binding("n", "select_no_items", "Select none"),
        Binding("r", "run_plan", "Run plan"),
        Binding("q", "app.quit", "Quit"),
    ]

    def __init__(self, *, dry_run: bool = False) -> None:
        super().__init__()
        self.state = PlanState.initial(ALL_SECTIONS)
        self.dry_run = dry_run
        self._executing = False
        self._keepalive = SudoKeepalive()
        self._sudo_acquired = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            with Vertical(id="sections-pane"):
                yield Static("Plan", id="pane-title-sections")
                yield ListView(
                    *[SectionRow(s, self.state) for s in ALL_SECTIONS],
                    id="section-list",
                )
            with VerticalScroll(id="detail-pane"):
                # Planning-mode widgets.
                yield Static("", id="detail-title", classes="plan-mode")
                yield Static("", id="detail-desc", classes="plan-mode")
                yield Static("", id="detail-items-host", classes="plan-mode")
                # Running-mode widgets — hidden until `r` is pressed.
                yield Static("", id="exec-progress", classes="exec-mode hidden")
                yield RichLog(
                    id="exec-log",
                    classes="exec-mode hidden",
                    wrap=True,
                    highlight=False,
                    markup=True,
                )
        yield Footer()

    async def on_mount(self) -> None:
        list_view = self.query_one("#section-list", ListView)
        list_view.focus()
        if list_view.children:
            await self._refresh_detail(list_view.highlighted_child)  # type: ignore[arg-type]

    async def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if self._executing:
            return
        await self._refresh_detail(event.item)  # type: ignore[arg-type]

    def _current_row(self) -> SectionRow | None:
        list_view = self.query_one("#section-list", ListView)
        return list_view.highlighted_child  # type: ignore[return-value]

    async def _refresh_detail(self, row: SectionRow | None) -> None:
        if row is None:
            return
        section = row.section
        title = Text(section.display_name, style="bold")
        self.query_one("#detail-title", Static).update(title)
        self.query_one("#detail-desc", Static).update(section.description)

        host = self.query_one("#detail-items-host", Static)
        await host.remove_children()

        if section.items_config:
            items = section.load_items()
            selected = self.state.enabled_items.get(section.slug, set())
            if items:
                selections = []
                for i in items:
                    label = Text(i.name)
                    if i.description:
                        label.append(f"  {i.description}", style="#6a737d")
                    selections.append(Selection(label, i.name, i.name in selected))
                sel_list = SelectionList[str](*selections)
                sel_list.section_slug = section.slug  # type: ignore[attr-defined]
                await host.mount(sel_list)
            else:
                await host.mount(Static(Text("(no items in TOML yet)", style="#6a737d")))

    # --- planning actions ------------------------------------------------

    def action_toggle_section(self) -> None:
        if self._executing:
            return
        row = self._current_row()
        if row is None:
            return
        self.state.toggle_section(row.section.slug)
        row.refresh_row()

    def action_focus_detail(self) -> None:
        try:
            sel = self.query_one(SelectionList)
        except Exception:
            return
        sel.focus()

    def action_focus_sections(self) -> None:
        self.query_one("#section-list", ListView).focus()

    async def action_select_all_items(self) -> None:
        if self._executing:
            return
        row = self._current_row()
        if row is None or not row.section.items_config:
            return
        items = row.section.load_items()
        self.state.set_items(row.section.slug, [i.name for i in items])
        await self._refresh_detail(row)
        row.refresh_row()

    async def action_select_no_items(self) -> None:
        if self._executing:
            return
        row = self._current_row()
        if row is None or not row.section.items_config:
            return
        self.state.set_items(row.section.slug, [])
        await self._refresh_detail(row)
        row.refresh_row()

    def on_selection_list_selected_changed(
        self, event: SelectionList.SelectedChanged[str]
    ) -> None:
        if self._executing:
            return
        widget = event.selection_list
        slug = getattr(widget, "section_slug", None)
        if not slug:
            return
        self.state.set_items(slug, widget.selected)
        try:
            row = self.query_one(f"#row-{slug}", SectionRow)
        except Exception:
            return
        row.refresh_row()

    # --- run plan --------------------------------------------------------

    async def action_run_plan(self) -> None:
        if self._executing:
            return
        self._executing = True
        self._enter_running_mode()

        log_widget = self.query_one("#exec-log", RichLog)
        progress_widget = self.query_one("#exec-progress", Static)

        log_path = Path.home() / "macsetup-last-run.log"
        _log_file = log_path.open("w", encoding="utf-8")
        _log_file.write(f"macsetup run started {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        def _strip_markup(message: object) -> str:
            if isinstance(message, Text):
                return message.plain
            return re.sub(r"\[.*?\]", "", str(message))

        def log(message) -> None:
            log_widget.write(message)
            _log_file.write(_strip_markup(message) + "\n")
            _log_file.flush()

        def progress(message) -> None:
            progress_widget.update(message)

        banner = "macsetup — dry-run preview" if self.dry_run else "macsetup — executing plan"
        log(Text(banner + "\n", style="bold #d4d4d4"))

        active_shell = DryRunShell(Shell(), log) if self.dry_run else Shell()
        executor = Executor(
            shell=active_shell,  # type: ignore[arg-type]
            log=log,
            progress=progress,
            suspend=self.app.suspend,
            ensure_sudo=self._ensure_sudo,
            state=self.state,
            keepalive=self._keepalive,
            dry_run=self.dry_run,
        )

        if not self.dry_run and self.state.is_section_enabled("mas"):
            log("[#d4d4d4]App Store installs need sudo — prompting now so the run isn't interrupted later.[/]")
            if not await self._ensure_sudo():
                log("  [#f44747]sudo not granted — App Store installs will likely fail[/]")

        results: dict[str, str] = {}
        try:
            for section in ALL_SECTIONS:
                if not self.state.is_section_enabled(section.slug):
                    log(f"[#6a737d]→ {section.display_name}: skipped[/]")
                    results[section.slug] = "skipped"
                    self._set_status(section.slug, "skipped")
                    continue

                self._set_status(section.slug, "running")
                progress(f"→ {section.display_name}")
                log(f"[#007acc]→ {section.display_name}[/]")

                runner = get_runner(section.slug)
                if runner is None:
                    log("  [#6a737d]no runner registered[/]")
                    results[section.slug] = "skipped"
                    self._set_status(section.slug, "skipped")
                    continue

                try:
                    ok = await runner(
                        section,
                        self.state.enabled_items.get(section.slug, set()),
                        executor,
                    )
                    if ok:
                        results[section.slug] = "ok"
                        self._set_status(section.slug, "ok")
                    else:
                        log("  [#f44747]failed[/]")
                        results[section.slug] = "failed"
                        self._set_status(section.slug, "failed")
                except Exception as exc:  # noqa: BLE001
                    log(f"  [#f44747]error: {exc}[/]")
                    results[section.slug] = "failed"
                    self._set_status(section.slug, "failed")
            progress("Plan complete")
            log(self._format_summary(results))
        finally:
            self._keepalive.stop()
            _log_file.close()

    def _set_status(self, slug: str, status: str) -> None:
        self.state.section_status[slug] = status
        try:
            self.query_one(f"#row-{slug}", SectionRow).refresh_row()
        except Exception:
            pass

    def _enter_running_mode(self) -> None:
        for w in self.query(".plan-mode"):
            w.add_class("hidden")
        for w in self.query(".exec-mode"):
            w.remove_class("hidden")

    async def _ensure_sudo(self) -> bool:
        if self._sudo_acquired:
            return True
        ok = await acquire_sudo(self.app.suspend)
        if ok:
            self._sudo_acquired = True
            self._keepalive.start()
        return ok

    def _format_summary(self, results: dict[str, str]) -> Text:
        ok = sum(1 for v in results.values() if v == "ok")
        skipped = sum(1 for v in results.values() if v == "skipped")
        failed = sum(1 for v in results.values() if v == "failed")

        text = Text()
        text.append("\nPlan complete  ", style="bold #d4d4d4")
        text.append(f"{ok}", style="bold #4ec9b0")
        text.append(" succeeded   ")
        text.append(f"{skipped}", style="#6a737d")
        text.append(" skipped   ")
        text.append(f"{failed}", style="bold #f44747" if failed else "#6a737d")
        text.append(" failed\n")

        if failed:
            text.append("\nFailures:\n", style="bold #f44747")
            for slug, status in results.items():
                if status == "failed":
                    section = SECTIONS_BY_SLUG.get(slug)
                    name = section.display_name if section else slug
                    text.append(f"  · {name}\n", style="#f44747")

        backup_dir = self._find_backup_dir()
        if backup_dir is not None:
            text.append("\nDotfile backup: ", style="#6a737d")
            text.append(f"{backup_dir}\n", style="#d4d4d4")

        guide = Path.home() / "MACSETUP-USAGE.html"
        if guide.exists():
            text.append("Usage guide:    ", style="#6a737d")
            text.append(f"{guide}\n", style="#d4d4d4")

        text.append("\nPress q to exit.", style="bold")
        return text

    def _find_backup_dir(self) -> Path | None:
        root = Path.home() / ".dotfile-backups"
        if not root.exists():
            return None
        subdirs = sorted([p for p in root.iterdir() if p.is_dir()])
        return subdirs[-1] if subdirs else None
