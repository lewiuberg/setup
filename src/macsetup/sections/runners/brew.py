"""Runners for the Homebrew family: rosetta, homebrew, taps, brews, casks, fonts.

All brew install commands stream their output to the TUI log. Detection always
runs first so re-runs report "already installed" rather than re-fetching.
"""
from __future__ import annotations

import platform
import subprocess

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner

HOMEBREW_INSTALL_CMD = (
    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
)


# ---------------------------------------------------------------------------
# Rosetta 2
# ---------------------------------------------------------------------------

def _is_apple_silicon() -> bool:
    return platform.machine() == "arm64"


async def _rosetta_installed(executor: Executor) -> bool:
    if not _is_apple_silicon():
        return True  # Not applicable
    result = await executor.shell.run(["/usr/sbin/pkgutil", "--pkgs=com.apple.pkg.RosettaUpdateAuto"])
    return result.ok and "RosettaUpdateAuto" in result.output


@register_runner("rosetta")
async def run_rosetta(section: Section, items: set[str], executor: Executor) -> bool:
    if not _is_apple_silicon():
        executor.log(f"  [#6a737d]{section.display_name}: not applicable on Intel[/]")
        return True
    if await _rosetta_installed(executor):
        executor.log(f"  [#4ec9b0]✓[/] {section.display_name}: already installed")
        return True
    executor.log(f"  installing Rosetta 2…")
    result = await executor.shell.stream(
        ["/usr/sbin/softwareupdate", "--install-rosetta", "--agree-to-license"],
        lambda line: executor.log(f"    {line}"),
    )
    return result == 0


# ---------------------------------------------------------------------------
# Homebrew itself
# ---------------------------------------------------------------------------

@register_runner("homebrew")
async def run_homebrew(section: Section, items: set[str], executor: Executor) -> bool:
    if executor.shell.has("brew"):
        executor.log(f"  [#4ec9b0]✓[/] Homebrew already installed")
    elif executor.dry_run:
        executor.log("  [#ce9178][dry-run][/] would run the Homebrew installer (curl install.sh)")
    else:
        executor.log("  installing Homebrew (will take a few minutes; yields the terminal)…")
        with executor.suspend():
            proc = subprocess.run(["/bin/bash", "-c", HOMEBREW_INSTALL_CMD], check=False)
        if proc.returncode != 0:
            executor.log(f"  [#f44747]Homebrew installer exited {proc.returncode}[/]")
            return False
        executor.log(f"  [#4ec9b0]✓[/] Homebrew installed")

    executor.log("  running brew update…")
    update = await executor.shell.stream(
        ["brew", "update"], lambda line: executor.log(f"    {line}")
    )
    if update != 0:
        executor.log(f"  [#ce9178]brew update exited {update} (continuing)[/]")

    executor.log("  running brew doctor…")
    doctor = await executor.shell.stream(
        ["brew", "doctor"], lambda line: executor.log(f"    {line}")
    )
    if doctor != 0:
        executor.log(f"  [#ce9178]brew doctor reported issues (continuing)[/]")

    return True


# ---------------------------------------------------------------------------
# Helpers shared by taps / brews / casks / fonts
# ---------------------------------------------------------------------------

async def _installed_taps(executor: Executor) -> set[str]:
    result = await executor.shell.run(["brew", "tap"])
    return set(result.output.strip().splitlines()) if result.ok else set()


async def _installed_formulae(executor: Executor) -> set[str]:
    result = await executor.shell.run(["brew", "list", "--formula", "-1"])
    return set(result.output.strip().splitlines()) if result.ok else set()


async def _installed_casks(executor: Executor) -> set[str]:
    result = await executor.shell.run(["brew", "list", "--cask", "-1"])
    return set(result.output.strip().splitlines()) if result.ok else set()


async def _require_brew(executor: Executor) -> bool:
    if not executor.shell.has("brew"):
        executor.log("  [#f44747]Homebrew not installed — run the Homebrew section first[/]")
        return False
    return True


# ---------------------------------------------------------------------------
# Taps
# ---------------------------------------------------------------------------

@register_runner("taps")
async def run_taps(section: Section, items: set[str], executor: Executor) -> bool:
    if not await _require_brew(executor):
        return False
    if not items:
        executor.log(f"  [#6a737d]no taps selected[/]")
        return True
    have = await _installed_taps(executor)
    total = len(items)
    for index, name in enumerate(sorted(items), start=1):
        if name in have:
            executor.log(f"  [{index}/{total}] [#4ec9b0]✓[/] {name} (already tapped)")
            continue
        executor.log(f"  [{index}/{total}] tapping {name}…")
        code = await executor.shell.stream(
            ["brew", "tap", name], lambda line: executor.log(f"      {line}")
        )
        if code != 0:
            executor.log(f"      [#f44747]failed[/]")
    return True


# ---------------------------------------------------------------------------
# Brew formulae and casks share a shape
# ---------------------------------------------------------------------------

async def _install_with_brew(
    section: Section,
    items: set[str],
    executor: Executor,
    *,
    cask: bool,
) -> bool:
    if not await _require_brew(executor):
        return False
    if not items:
        executor.log(f"  [#6a737d]no items selected[/]")
        return True
    have = await (_installed_casks(executor) if cask else _installed_formulae(executor))
    install_args = ["brew", "install"] + (["--cask"] if cask else [])
    total = len(items)
    for index, name in enumerate(sorted(items), start=1):
        if name in have:
            executor.log(f"  [{index}/{total}] [#4ec9b0]✓[/] {name} (already installed)")
            continue
        executor.log(f"  [{index}/{total}] installing {name}…")
        code = await executor.shell.stream(
            install_args + [name], lambda line: executor.log(f"      {line}")
        )
        if code != 0:
            executor.log(f"      [#f44747]failed (exit {code})[/]")
    return True


@register_runner("brews")
async def run_brews(section: Section, items: set[str], executor: Executor) -> bool:
    return await _install_with_brew(section, items, executor, cask=False)


@register_runner("casks")
async def run_casks(section: Section, items: set[str], executor: Executor) -> bool:
    return await _install_with_brew(section, items, executor, cask=True)


@register_runner("fonts")
async def run_fonts(section: Section, items: set[str], executor: Executor) -> bool:
    # Fonts are casks too; route through the same path.
    return await _install_with_brew(section, items, executor, cask=True)


# ---------------------------------------------------------------------------
# Mac App Store (mas)
# ---------------------------------------------------------------------------

@register_runner("mas")
async def run_mas(section: Section, items: set[str], executor: Executor) -> bool:
    mas_path = executor.shell.which("mas")
    if mas_path is None:
        executor.log("  [#f44747]mas not installed (add `mas` to brews.toml)[/]")
        return False

    if not items:
        executor.log("  [#6a737d]no App Store apps selected[/]")
        return True

    installed = await executor.shell.run([mas_path, "list"])
    installed_ids: set[str] = set()
    if installed.ok:
        for line in installed.output.splitlines():
            parts = line.split(" ", 1)
            if parts:
                installed_ids.add(parts[0])

    # Resolve item names back to their App Store IDs (stored under `extras.id`).
    name_to_id = {i.name: str(i.extras.get("id", "")) for i in section.load_items()}
    total = len(items)
    # `sudo -n mas install`: mas 7 re-execs itself under sudo internally, which
    # opens /dev/tty for the password prompt and collides with Textual's raw
    # mode. By calling sudo ourselves (using the timestamp pre-acquired via the
    # osascript dialog), mas sees it is already root and skips the re-exec.
    # `-n` makes sudo fail fast instead of prompting if the timestamp expired.
    for index, name in enumerate(sorted(items), start=1):
        app_id = name_to_id.get(name)
        if not app_id:
            executor.log(f"  [{index}/{total}] [#ce9178]{name}: missing `id` in TOML, skipped[/]")
            continue
        if app_id in installed_ids:
            executor.log(f"  [{index}/{total}] [#4ec9b0]✓[/] {name} (already installed)")
            continue
        executor.log(f"  [{index}/{total}] installing {name} (id {app_id})…")
        code = await executor.shell.stream(
            ["sudo", "-n", mas_path, "install", app_id],
            lambda line: executor.log(f"      {line}"),
        )
        if code != 0:
            executor.log(f"      [#f44747]failed (exit {code})[/]")
    return True
