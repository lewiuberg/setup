"""Runner for Python tooling: confirm uv is on PATH, apply Poetry's
version-aware virtualenv config.

uv itself ships via the brews section. Poetry installation is opt-in; users
enable the `poetry` brew entry. If Poetry is present, we apply the right
`virtualenvs` config for the running version (the 2.x release removed
`prefer-active-python`).
"""
from __future__ import annotations

import re

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner

VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")


def _parse_poetry_version(version_output: str) -> tuple[int, int, int] | None:
    match = VERSION_RE.search(version_output)
    if not match:
        return None
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3) or 0)
    return major, minor, patch


@register_runner("python_tools")
async def run_python_tools(section: Section, items: set[str], executor: Executor) -> bool:
    if executor.shell.has("uv"):
        executor.log("  [#4ec9b0]✓[/] uv on PATH")
    else:
        executor.log("  [#ce9178]uv not on PATH — add `uv` to brews.toml and run the brews section[/]")

    if not executor.shell.has("poetry"):
        executor.log("  [#6a737d]Poetry not installed (opt-in; tick `poetry` in brews.toml to add it)[/]")
        return True

    version_result = await executor.shell.run(["poetry", "--version"])
    if not version_result.ok:
        executor.log(f"  [#f44747]poetry --version failed: {version_result.output.strip()}[/]")
        return False

    parsed = _parse_poetry_version(version_result.output)
    if parsed is None:
        executor.log(f"  [#ce9178]could not parse Poetry version: {version_result.output.strip()}[/]")
        return False
    major, minor, patch = parsed
    version_str = f"{major}.{minor}.{patch}"

    if major < 2:
        executor.log(f"  Poetry {version_str} < 2.0 — setting virtualenvs.prefer-active-python=true")
        configure = await executor.shell.run(
            ["poetry", "config", "virtualenvs.prefer-active-python", "true"]
        )
        if not configure.ok:
            executor.log(f"  [#f44747]failed: {configure.output.strip()}[/]")
            return False
        return True

    executor.log(
        f"  Poetry {version_str} >= 2.0 — `prefer-active-python` removed, default behaviour is correct"
    )
    return True
