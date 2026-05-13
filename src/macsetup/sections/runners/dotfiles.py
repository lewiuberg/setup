"""Runner for the dotfiles section: backup existing files, render templates."""
from __future__ import annotations

from pathlib import Path

from macsetup.core.config import load_section
from macsetup.core.dotfiles import backup_existing, render, write
from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner

ZSHRC = Path.home() / ".zshrc"
ZPROFILE = Path.home() / ".zprofile"
WARPRC = Path.home() / ".warprc"


@register_runner("dotfiles")
async def run_dotfiles(section: Section, items: set[str], executor: Executor) -> bool:
    state = executor.state
    enabled = state.enabled_sections
    selected_brews = state.enabled_items.get("brews", set())

    extra_plugins: list[str] = []
    if "poetry" in selected_brews:
        extra_plugins.append("poetry")

    context = {
        "include_mise": "mise" in enabled or "mise" in selected_brews,
        "include_poetry": "poetry" in selected_brews,
        "include_uv": "uv" in selected_brews,
        "extra_plugins": extra_plugins,
    }

    warprc_items = load_section("warprc")
    shortcuts = [(i.name, str(i.extras.get("path", ""))) for i in warprc_items if i.extras.get("path")]

    if executor.dry_run:
        existing = [str(p) for p in (ZSHRC, ZPROFILE, WARPRC) if p.exists()]
        if existing:
            executor.log(
                f"  [#ce9178][dry-run][/] would back up {len(existing)} existing file(s) "
                f"to ~/.dotfile-backups/<timestamp>/: {', '.join(existing)}"
            )
        executor.log(f"  [#ce9178][dry-run][/] would write {ZSHRC}")
        executor.log(f"  [#ce9178][dry-run][/] would write {ZPROFILE}")
        executor.log(f"  [#ce9178][dry-run][/] would write {WARPRC} ({len(shortcuts)} shortcuts)")
        return True

    # Back up existing dotfiles atomically.
    backup_dir = backup_existing([ZSHRC, ZPROFILE, WARPRC])
    if backup_dir is not None:
        executor.log(f"  backed up existing dotfiles → {backup_dir}")

    zshrc_text = render("zshrc.j2", context)
    write(zshrc_text, ZSHRC)
    executor.log(f"  [#4ec9b0]✓[/] wrote {ZSHRC}")

    zprofile_text = render("zprofile.j2", {})
    write(zprofile_text, ZPROFILE)
    executor.log(f"  [#4ec9b0]✓[/] wrote {ZPROFILE}")

    warprc_text = render("warprc.j2", {"shortcuts": shortcuts})
    write(warprc_text, WARPRC)
    executor.log(f"  [#4ec9b0]✓[/] wrote {WARPRC} ({len(shortcuts)} shortcuts)")

    return True
