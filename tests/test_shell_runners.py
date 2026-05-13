from __future__ import annotations

import pytest

from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


@pytest.mark.asyncio
async def test_mise_skipped_when_binary_missing() -> None:
    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["mise"](SECTIONS_BY_SLUG["mise"], {"python"}, executor)
    assert ok is False
    assert any("mise not on PATH" in line for line in logs)


@pytest.mark.asyncio
async def test_mise_streams_one_command_per_runtime() -> None:
    shell = FakeShell(installed={"mise"})
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["mise"](SECTIONS_BY_SLUG["mise"], {"python", "node"}, executor)
    assert ok
    # Sorted iteration: node before python.
    assert ("mise", "use", "--global", "node@lts") in shell.streams
    assert ("mise", "use", "--global", "python@latest") in shell.streams


@pytest.mark.asyncio
async def test_mise_skipped_when_no_runtimes_selected() -> None:
    shell = FakeShell(installed={"mise"})
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["mise"](SECTIONS_BY_SLUG["mise"], set(), executor)
    assert ok
    assert shell.streams == []
    assert any("no runtimes selected" in line for line in logs)


def test_zsh_runners_registered() -> None:
    for slug in ("oh_my_zsh", "powerlevel10k", "zsh_plugins"):
        assert slug in RUNNERS, f"{slug} not registered"


def test_brew_family_runners_registered() -> None:
    for slug in ("rosetta", "homebrew", "taps", "brews", "casks", "fonts", "mas"):
        assert slug in RUNNERS, f"{slug} not registered"
