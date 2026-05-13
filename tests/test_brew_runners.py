from __future__ import annotations

import pytest

from macsetup.core.shell import CommandResult
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


def _brews_section():
    return SECTIONS_BY_SLUG["brews"]


def _casks_section():
    return SECTIONS_BY_SLUG["casks"]


def _taps_section():
    return SECTIONS_BY_SLUG["taps"]


def _homebrew_section():
    return SECTIONS_BY_SLUG["homebrew"]


@pytest.mark.asyncio
async def test_brews_skips_already_installed() -> None:
    shell = FakeShell(installed={"brew"})
    shell.canned[("brew", "list", "--formula", "-1")] = CommandResult(0, "git\nfzf\n")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["brews"](_brews_section(), {"git", "fzf", "ripgrep"}, executor)
    assert ok
    # Two were already installed, one was streamed for install.
    assert shell.streams == [("brew", "install", "ripgrep")]
    assert any("git (already installed)" in line for line in logs)
    assert any("installing ripgrep" in line for line in logs)


@pytest.mark.asyncio
async def test_brews_fails_when_brew_missing() -> None:
    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["brews"](_brews_section(), {"git"}, executor)
    assert ok is False
    assert any("Homebrew not installed" in line for line in logs)


@pytest.mark.asyncio
async def test_brews_skips_when_no_items_selected() -> None:
    shell = FakeShell(installed={"brew"})
    shell.canned[("brew", "list", "--formula", "-1")] = CommandResult(0, "")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["brews"](_brews_section(), set(), executor)
    assert ok
    assert shell.streams == []
    assert any("no items selected" in line for line in logs)


@pytest.mark.asyncio
async def test_casks_uses_cask_flag() -> None:
    shell = FakeShell(installed={"brew"})
    shell.canned[("brew", "list", "--cask", "-1")] = CommandResult(0, "")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["casks"](_casks_section(), {"warp"}, executor)
    assert ok
    assert shell.streams == [("brew", "install", "--cask", "warp")]


@pytest.mark.asyncio
async def test_taps_skips_already_tapped() -> None:
    shell = FakeShell(installed={"brew"})
    shell.canned[("brew", "tap",)] = CommandResult(0, "hashicorp/tap\n")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["taps"](_taps_section(), {"hashicorp/tap", "heroku/brew"}, executor)
    assert ok
    assert shell.streams == [("brew", "tap", "heroku/brew")]


@pytest.mark.asyncio
async def test_fonts_routes_through_cask_path() -> None:
    shell = FakeShell(installed={"brew"})
    shell.canned[("brew", "list", "--cask", "-1")] = CommandResult(0, "font-meslo-lg-nerd-font\n")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    fonts_section = SECTIONS_BY_SLUG["fonts"]
    ok = await RUNNERS["fonts"](fonts_section, {"font-meslo-lg-nerd-font", "font-fira-code"}, executor)
    assert ok
    assert shell.streams == [("brew", "install", "--cask", "font-fira-code")]


@pytest.mark.asyncio
async def test_homebrew_already_installed_runs_update_and_doctor() -> None:
    shell = FakeShell(installed={"brew"})
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["homebrew"](_homebrew_section(), set(), executor)
    assert ok
    # Streamed brew update + brew doctor.
    assert ("brew", "update") in shell.streams
    assert ("brew", "doctor") in shell.streams
    assert any("already installed" in line for line in logs)
