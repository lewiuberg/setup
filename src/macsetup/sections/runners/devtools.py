"""Runner for mise + runtimes. mise itself is installed via the Brew formula
list (entry `mise` in brews.toml); this runner activates per-runtime versions.
"""
from __future__ import annotations

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner


@register_runner("mise")
async def run_mise(section: Section, items: set[str], executor: Executor) -> bool:
    if not executor.shell.has("mise"):
        executor.log("  [#f44747]mise not on PATH — install via brews (mise) first[/]")
        return False
    if not items:
        executor.log("  [#6a737d]no runtimes selected[/]")
        return True

    name_to_version = {i.name: str(i.extras.get("version", "latest")) for i in section.load_items()}
    total = len(items)
    for index, name in enumerate(sorted(items), start=1):
        version = name_to_version.get(name, "latest")
        spec = f"{name}@{version}"
        executor.log(f"  [{index}/{total}] installing {spec}…")
        code = await executor.shell.stream(
            ["mise", "use", "--global", spec],
            lambda line: executor.log(f"      {line}"),
        )
        if code != 0:
            executor.log(f"      [#f44747]failed (exit {code})[/]")
    return True
