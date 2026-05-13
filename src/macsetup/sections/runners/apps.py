"""Runners for sections that just open URLs: Raycast extensions and manual app downloads."""
from __future__ import annotations

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner


async def _open_urls(section: Section, items: set[str], executor: Executor, *, kind: str) -> bool:
    if not items:
        executor.log(f"  [#6a737d]no {kind} selected[/]")
        return True
    name_to_url = {i.name: str(i.extras.get("url", "")) for i in section.load_items()}
    total = len(items)
    for index, name in enumerate(sorted(items), start=1):
        url = name_to_url.get(name, "")
        if not url:
            executor.log(f"  [{index}/{total}] [#ce9178]{name}: no URL in TOML, skipped[/]")
            continue
        executor.log(f"  [{index}/{total}] opening {name} → {url}")
        await executor.shell.run(["open", url])
    executor.log(f"  [#4ec9b0]✓[/] opened {total} {kind} page(s) — install each then resume the wizard")
    return True


@register_runner("raycast")
async def run_raycast(section: Section, items: set[str], executor: Executor) -> bool:
    return await _open_urls(section, items, executor, kind="Raycast extensions")


@register_runner("manual_apps")
async def run_manual_apps(section: Section, items: set[str], executor: Executor) -> bool:
    return await _open_urls(section, items, executor, kind="manual apps")
