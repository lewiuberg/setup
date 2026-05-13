"""Live system detection probes.

No state file. Every check hits the real system so that re-runs always
reflect current truth.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Union

from macsetup.core.shell import run_capture


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def path_exists(path: Union[str, os.PathLike[str]]) -> bool:
    return Path(path).expanduser().exists()


def is_symlink_to(
    link: Union[str, os.PathLike[str]],
    target: Union[str, os.PathLike[str]],
) -> bool:
    p = Path(link).expanduser()
    if not p.is_symlink():
        return False
    return Path(os.readlink(p)).resolve() == Path(target).expanduser().resolve()


def line_in_file(needle: str, path: Union[str, os.PathLike[str]]) -> bool:
    p = Path(path).expanduser()
    if not p.exists():
        return False
    try:
        return any(needle in line for line in p.read_text().splitlines())
    except (UnicodeDecodeError, OSError):
        return False


async def brew_installed(formula: str) -> bool:
    if not command_exists("brew"):
        return False
    return (await run_capture(["brew", "list", "--formula", formula])).ok


async def cask_installed(cask: str) -> bool:
    if not command_exists("brew"):
        return False
    return (await run_capture(["brew", "list", "--cask", cask])).ok


async def vscode_extension_installed(extension_id: str) -> bool:
    if not command_exists("code"):
        return False
    result = await run_capture(["code", "--list-extensions"])
    if not result.ok:
        return False
    return extension_id.lower() in {
        line.strip().lower() for line in result.stdout.splitlines() if line.strip()
    }


# Batch lookup helpers — one subprocess per section instead of one per item.
# Sections call these once at the top of detect() and intersect against
# their TOML's item names.


async def installed_brews() -> set[str]:
    if not command_exists("brew"):
        return set()
    result = await run_capture(["brew", "list", "--formula"])
    if not result.ok:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


async def installed_casks() -> set[str]:
    if not command_exists("brew"):
        return set()
    result = await run_capture(["brew", "list", "--cask"])
    if not result.ok:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


async def installed_taps() -> set[str]:
    if not command_exists("brew"):
        return set()
    result = await run_capture(["brew", "tap"])
    if not result.ok:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


async def installed_vscode_extensions() -> set[str]:
    if not command_exists("code"):
        return set()
    result = await run_capture(["code", "--list-extensions"])
    if not result.ok:
        return set()
    return {line.strip().lower() for line in result.stdout.splitlines() if line.strip()}
