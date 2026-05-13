from __future__ import annotations

import pytest

from macsetup.core.shell import CommandResult
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


@pytest.mark.asyncio
async def test_vscode_fails_when_code_cli_missing() -> None:
    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["vscode"](SECTIONS_BY_SLUG["vscode"], {"ms-python.python"}, executor)
    assert ok is False
    assert any("code` CLI not on PATH" in line for line in logs)


@pytest.mark.asyncio
async def test_vscode_skips_install_when_all_present() -> None:
    shell = FakeShell(installed={"code"})
    shell.canned[("code", "--list-extensions")] = CommandResult(
        0, "ms-python.python\nCharliermarsh.ruff\n"
    )
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["vscode"](
        SECTIONS_BY_SLUG["vscode"],
        {"ms-python.python", "charliermarsh.ruff"},
        executor,
    )
    assert ok
    assert shell.streams == []
    assert any("all baseline extensions already present" in line for line in logs)


@pytest.mark.asyncio
async def test_vscode_installs_missing(monkeypatch) -> None:
    shell = FakeShell(installed={"code"})
    shell.canned[("code", "--list-extensions")] = CommandResult(
        0, "ms-python.python\n"
    )
    logs: list[str] = []
    executor = make_executor(shell, logs)

    # Suppress the interactive `input()` prompt by monkeypatching builtins.
    monkeypatch.setattr("builtins.input", lambda *_: "")
    # Suppress the subprocess.run("open ...") call.
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: None)

    ok = await RUNNERS["vscode"](
        SECTIONS_BY_SLUG["vscode"],
        {"ms-python.python", "charliermarsh.ruff", "eamodio.gitlens"},
        executor,
    )
    assert ok
    # Two extensions were missing (ms-python is installed).
    expected_streams = {
        ("code", "--install-extension", "charliermarsh.ruff"),
        ("code", "--install-extension", "eamodio.gitlens"),
    }
    assert set(shell.streams) == expected_streams


@pytest.mark.asyncio
async def test_vscode_skips_when_no_extensions_selected() -> None:
    shell = FakeShell(installed={"code"})
    shell.canned[("code", "--list-extensions")] = CommandResult(0, "")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["vscode"](SECTIONS_BY_SLUG["vscode"], set(), executor)
    assert ok
    assert any("no extensions selected" in line for line in logs)
