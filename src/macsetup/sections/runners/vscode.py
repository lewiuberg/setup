"""VS Code section runner.

Flow:
1. Confirm `code` is on PATH (installed via casks).
2. Open VS Code so Settings Sync can run.
3. Suspend the TUI and prompt the user to confirm sync has completed.
4. Diff `code --list-extensions` against the baseline TOML.
5. Install any missing extensions via `code --install-extension`.
"""
from __future__ import annotations

import subprocess

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner


async def _installed_extensions(executor: Executor) -> set[str]:
    result = await executor.shell.run(["code", "--list-extensions"])
    if not result.ok:
        return set()
    return {line.strip().lower() for line in result.output.splitlines() if line.strip()}


@register_runner("vscode")
async def run_vscode(section: Section, items: set[str], executor: Executor) -> bool:
    if not executor.shell.has("code"):
        executor.log(
            "  [#f44747]`code` CLI not on PATH — install Visual Studio Code "
            "(casks → visual-studio-code) then run Shell Command: Install 'code' command in PATH[/]"
        )
        return False

    if not items:
        executor.log("  [#6a737d]no extensions selected[/]")
        return True

    wanted = {i.lower() for i in items}
    installed = await _installed_extensions(executor)
    missing = sorted(wanted - installed)
    if not missing:
        executor.log("  [#4ec9b0]✓[/] all baseline extensions already present")
        return True

    # Open VS Code so Settings Sync gets a chance to fill these in before we
    # install them by hand.
    if executor.dry_run:
        executor.log(
            f"  [#ce9178][dry-run][/] would open VS Code and prompt for Settings Sync, "
            f"then install {len(missing)} missing extension(s)"
        )
        return True

    executor.log(
        f"  {len(missing)} extension(s) missing — opening VS Code so Settings Sync can run…"
    )
    with executor.suspend():
        subprocess.run(["open", "-a", "Visual Studio Code"], check=False)
        input(
            "\nSign in to Visual Studio Code Settings Sync if you haven't yet, "
            "then return to this terminal and press Enter to continue. "
        )

    after_sync = await _installed_extensions(executor)
    still_missing = sorted(wanted - after_sync)
    if not still_missing:
        executor.log(
            "  [#4ec9b0]✓[/] Settings Sync filled in everything; nothing to install"
        )
        return True

    executor.log(f"  installing {len(still_missing)} extension(s)…")
    for index, ext in enumerate(still_missing, start=1):
        code = await executor.shell.stream(
            ["code", "--install-extension", ext],
            lambda line: executor.log(f"    [{index}/{len(still_missing)}] {line}"),
        )
        if code != 0:
            executor.log(f"    [#f44747]{ext} failed (exit {code})[/]")
    return True
