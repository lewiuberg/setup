"""Python project/dependency managers — uv (primary) and Poetry (legacy).

uv is installed via Brews section; this section verifies. Poetry is
optional and uses the version-aware fix that addresses the bug in the
legacy script (Poetry 2.x removed `virtualenvs.prefer-active-python`).
"""

from __future__ import annotations

import re

from macsetup.core.config import Item, load_items
from macsetup.core.detect import command_exists
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run, run_capture
from macsetup.sections.base import Emit, Section, SectionStatus, Status


POETRY_INSTALL_URL = "https://install.python-poetry.org"


async def _poetry_version() -> tuple[int, int, int] | None:
    if not command_exists("poetry"):
        return None
    result = await run_capture(["poetry", "--version"])
    if not result.ok:
        return None
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", result.stdout)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


class PythonToolsSection(Section):
    name = "Python tools"
    description = "uv (primary) + Poetry (legacy projects only)"
    config_file = "python_tools.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        installed = 0
        for item in items:
            if command_exists(item.name):
                installed += 1
        if installed == len(items):
            return SectionStatus(Status.DONE, installed, len(items))
        if installed == 0:
            return SectionStatus(Status.PENDING, 0, len(items))
        return SectionStatus(Status.PARTIAL, installed, len(items))

    async def install(self, items: list[Item], emit: Emit) -> None:
        for item in items:
            if item.name == "uv":
                if command_exists("uv"):
                    await emit("uv already installed (managed by Brews section)")
                    continue
                await emit(
                    "uv is installed by the Brews section — tick it there and re-run"
                )
                continue
            if item.name == "poetry":
                if command_exists("poetry"):
                    version = await _poetry_version()
                    await emit(f"Poetry {version} already installed")
                    await self._apply_poetry_config(version, emit)
                    continue
                await emit("Installing Poetry (legacy projects)…")
                result = await run(
                    [
                        "bash",
                        "-c",
                        f"curl -sSL {POETRY_INSTALL_URL} | python3 -",
                    ],
                    on_line=emit,
                )
                if not result.ok:
                    await emit(f"Poetry install failed: {result.stderr.strip()}")
                    continue
                version = await _poetry_version()
                await emit(f"Poetry {version} installed")
                await self._apply_poetry_config(version, emit)
                continue
            await emit(f"unknown python tool: {item.name}")

    async def _apply_poetry_config(
        self,
        version: tuple[int, int, int] | None,
        emit: Emit,
    ) -> None:
        """Version-aware Poetry config.

        Fixes the bug in the legacy script: Poetry 2.x removed the
        `virtualenvs.prefer-active-python` setting. Setting it raises an
        error that set -e turned into a fatal script abort.
        """
        if version is None:
            await emit("Could not determine Poetry version; skipping config")
            return
        if version < (2, 0, 0):
            await emit("Poetry < 2.0: setting virtualenvs.prefer-active-python true")
            await run(
                ["poetry", "config", "virtualenvs.prefer-active-python", "true"],
                on_line=emit,
            )
        else:
            await emit(
                f"Poetry {version[0]}.{version[1]}.{version[2]}: "
                "skipping prefer-active-python (removed in Poetry 2.0); "
                "default behaviour already uses the active Python."
            )
