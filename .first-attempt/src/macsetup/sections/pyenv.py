"""pyenv — Python version manager.

Detects installed Python versions via `pyenv versions`. Installs missing
versions from config/python_tools.toml [pyenv].versions.

Explicitly never runs `pyenv global` — use `pyenv local <ver>` per project
(.python-version file) or `pyenv shell <ver>` per shell session.
"""

from __future__ import annotations

from pathlib import Path

import tomlkit

from macsetup.core.config import Item
from macsetup.core.detect import command_exists
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run, run_capture
from macsetup.sections.base import Emit, Section, SectionStatus, Status


PYENV_GLOBAL_MARKER = Path.home() / ".pyenv" / "version"


def _wanted_versions() -> list[str]:
    raw = tomlkit.parse((CONFIG_DIR / "python_tools.toml").read_text())
    pyenv_table = raw.get("pyenv", {})
    return [str(v) for v in pyenv_table.get("versions", [])]


async def _installed_versions() -> set[str]:
    if not command_exists("pyenv"):
        return set()
    result = await run_capture(["pyenv", "versions", "--bare"])
    if not result.ok:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


class PyenvSection(Section):
    name = "pyenv"
    description = "Python version manager (no global pin set)"

    async def detect(self) -> SectionStatus:
        if not command_exists("pyenv"):
            return SectionStatus(Status.PENDING, 0, 1, "pyenv brew formula missing")
        wanted = _wanted_versions()
        installed = await _installed_versions()
        count = sum(1 for v in wanted if v in installed)
        total = len(wanted)
        message = ""
        if PYENV_GLOBAL_MARKER.exists():
            message = "⚠ ~/.pyenv/version exists — pyenv global is set"
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0, message)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total, message)
        if count == total:
            return SectionStatus(Status.DONE, count, total, message)
        return SectionStatus(Status.PARTIAL, count, total, message)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not command_exists("pyenv"):
            await emit("pyenv brew formula missing — run the Brews section first")
            return
        wanted = _wanted_versions()
        installed = await _installed_versions()
        for version in wanted:
            if version in installed:
                await emit(f"already installed: Python {version}")
                continue
            await emit(f"pyenv install {version}")
            result = await run(["pyenv", "install", "--skip-existing", version], on_line=emit)
            if not result.ok:
                await emit(f"failed: Python {version}: {result.stderr.strip()}")
        if PYENV_GLOBAL_MARKER.exists():
            await emit(
                f"NOTE: {PYENV_GLOBAL_MARKER} exists (pyenv global is set). "
                "macsetup never sets global; delete this file to drop back to "
                "system Python, or use `pyenv local <ver>` per project."
            )
