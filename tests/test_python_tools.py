from __future__ import annotations

import pytest

from macsetup.core.shell import CommandResult
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS
from macsetup.sections.runners.python_tools import _parse_poetry_version

from tests.fakes import FakeShell, make_executor


def test_parse_poetry_version_handles_common_outputs() -> None:
    assert _parse_poetry_version("Poetry (version 1.8.3)") == (1, 8, 3)
    assert _parse_poetry_version("Poetry (version 2.0.0)") == (2, 0, 0)
    assert _parse_poetry_version("Poetry version 1.7") == (1, 7, 0)
    assert _parse_poetry_version("nope") is None


@pytest.mark.asyncio
async def test_python_tools_skips_poetry_when_absent() -> None:
    shell = FakeShell(installed={"uv"})
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["python_tools"](SECTIONS_BY_SLUG["python_tools"], set(), executor)
    assert ok
    assert any("uv on PATH" in line for line in logs)
    assert any("Poetry not installed" in line for line in logs)
    assert shell.runs == []  # no poetry calls


@pytest.mark.asyncio
async def test_python_tools_applies_prefer_active_python_for_v1() -> None:
    shell = FakeShell(installed={"uv", "poetry"})
    shell.canned[("poetry", "--version")] = CommandResult(0, "Poetry (version 1.8.3)")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["python_tools"](SECTIONS_BY_SLUG["python_tools"], set(), executor)
    assert ok
    assert ("poetry", "config", "virtualenvs.prefer-active-python", "true") in shell.runs


@pytest.mark.asyncio
async def test_python_tools_skips_config_for_v2() -> None:
    shell = FakeShell(installed={"uv", "poetry"})
    shell.canned[("poetry", "--version")] = CommandResult(0, "Poetry (version 2.0.1)")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["python_tools"](SECTIONS_BY_SLUG["python_tools"], set(), executor)
    assert ok
    assert ("poetry", "config", "virtualenvs.prefer-active-python", "true") not in shell.runs
    assert any(">= 2.0" in line for line in logs)
