"""Final wizard step: render ~/MACSETUP-USAGE.html templated by selections, open it."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from macsetup.core.config import load_section
from macsetup.core.dotfiles import render, write
from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import register_runner
from macsetup.sections.runners.python_tools import _parse_poetry_version

GUIDE_PATH = Path.home() / "MACSETUP-USAGE.html"


async def _detect_poetry_v2(executor: Executor) -> bool:
    if not executor.shell.has("poetry"):
        return False
    result = await executor.shell.run(["poetry", "--version"])
    if not result.ok:
        return False
    parsed = _parse_poetry_version(result.output)
    return parsed is not None and parsed[0] >= 2


@register_runner("html_guide")
async def run_html_guide(section: Section, items: set[str], executor: Executor) -> bool:
    state = executor.state
    enabled = state.enabled_sections
    selected_brews = state.enabled_items.get("brews", set())
    selected_runtimes = state.enabled_items.get("mise", set())
    selected_raycast = state.enabled_items.get("raycast", set())

    # mise runtimes that were actually selected (name → version).
    runtime_versions = {
        i.name: str(i.extras.get("version", "latest"))
        for i in SECTIONS_BY_SLUG["mise"].load_items()
    }
    mise_runtimes = [(name, runtime_versions.get(name, "latest")) for name in sorted(selected_runtimes)]

    # Raycast extension entries (name, url) for installed ones.
    raycast_lookup = {
        i.name: str(i.extras.get("url", "")) for i in SECTIONS_BY_SLUG["raycast"].load_items()
    }
    raycast_extensions = [(name, raycast_lookup.get(name, "")) for name in sorted(selected_raycast)]

    # Warp shortcuts always render if dotfiles was enabled.
    warp_shortcuts: list[tuple[str, str]] = []
    if "dotfiles" in enabled:
        for entry in load_section("warprc"):
            path = str(entry.extras.get("path", ""))
            if path:
                warp_shortcuts.append((entry.name, path))

    context = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "include_mise": "mise" in enabled or "mise" in selected_brews,
        "include_uv": "uv" in selected_brews,
        "include_poetry": "poetry" in selected_brews,
        "poetry_v2": await _detect_poetry_v2(executor),
        "include_github_auth": "github_auth" in enabled,
        "include_azure_devops": "azure_devops" in enabled,
        "mise_runtimes": mise_runtimes,
        "warp_shortcuts": warp_shortcuts,
        "raycast_extensions": raycast_extensions,
    }
    if executor.dry_run:
        executor.log(f"  [#ce9178][dry-run][/] would write {GUIDE_PATH} and open it in the browser")
        return True

    html = render("usage_guide.html.j2", context)
    write(html, GUIDE_PATH)
    executor.log(f"  [#4ec9b0]✓[/] wrote {GUIDE_PATH}")
    await executor.shell.run(["open", str(GUIDE_PATH)])
    executor.log("  opened in browser")
    return True
