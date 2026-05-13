"""Verify that bypassing-runner paths respect `executor.dry_run`.

These are the spots that don't go through `Shell` (so the DryRunShell wrapper
doesn't catch them): the Homebrew bootstrap, p10k configurator, gh auth login,
ssh-keygen, the VS Code open+input flow, dotfile writes, and the HTML guide.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from macsetup.core.shell import CommandResult
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


@pytest.mark.asyncio
async def test_homebrew_dryrun_skips_bootstrap_when_brew_missing() -> None:
    shell = FakeShell(installed=set())  # brew NOT installed
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)

    ok = await RUNNERS["homebrew"](SECTIONS_BY_SLUG["homebrew"], set(), executor)
    assert ok
    assert any("[dry-run]" in line and "Homebrew installer" in line for line in logs)


@pytest.mark.asyncio
async def test_github_auth_dryrun_skips_login() -> None:
    shell = FakeShell(installed={"gh"})
    shell.canned[("gh", "auth", "status")] = CommandResult(1, "not logged in")
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)

    ok = await RUNNERS["github_auth"](SECTIONS_BY_SLUG["github_auth"], set(), executor)
    assert ok
    assert any("[dry-run]" in line and "gh auth login" in line for line in logs)


@pytest.mark.asyncio
async def test_azure_devops_dryrun_skips_keygen(monkeypatch) -> None:
    # Force "no key found" so we hit the keygen branch.
    monkeypatch.setattr(
        "macsetup.sections.runners.auth.SSH_KEY_CANDIDATES",
        (Path("/nonexistent/id_ed25519.pub"),),
    )
    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)

    ok = await RUNNERS["azure_devops"](SECTIONS_BY_SLUG["azure_devops"], set(), executor)
    assert ok
    assert any("[dry-run]" in line and "ssh-keygen" in line for line in logs)


@pytest.mark.asyncio
async def test_vscode_dryrun_skips_open_and_install() -> None:
    shell = FakeShell(installed={"code"})
    shell.canned[("code", "--list-extensions")] = CommandResult(0, "")  # nothing installed
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)

    ok = await RUNNERS["vscode"](
        SECTIONS_BY_SLUG["vscode"],
        {"ms-python.python", "eamodio.gitlens"},
        executor,
    )
    assert ok
    # No `code --install-extension` streams should have run.
    assert shell.streams == []
    assert any("[dry-run]" in line and "VS Code" in line for line in logs)


@pytest.mark.asyncio
async def test_dotfiles_dryrun_does_not_write_or_backup(tmp_path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    pre_zshrc = fake_home / ".zshrc"
    pre_zshrc.write_text("# pre-existing")

    monkeypatch.setattr("macsetup.sections.runners.dotfiles.ZSHRC", fake_home / ".zshrc")
    monkeypatch.setattr("macsetup.sections.runners.dotfiles.ZPROFILE", fake_home / ".zprofile")
    monkeypatch.setattr("macsetup.sections.runners.dotfiles.WARPRC", fake_home / ".warprc")

    shell = FakeShell()
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)
    # Mark state so the templates would render.
    executor.state.enabled_sections = {"mise", "dotfiles"}

    ok = await RUNNERS["dotfiles"](SECTIONS_BY_SLUG["dotfiles"], set(), executor)
    assert ok
    # Pre-existing file untouched.
    assert pre_zshrc.read_text() == "# pre-existing"
    # No new files written.
    assert not (fake_home / ".zprofile").exists()
    assert not (fake_home / ".warprc").exists()
    # No backup directory created under tmp_path (default backup target is $HOME — fine).
    assert any("[dry-run]" in line for line in logs)


@pytest.mark.asyncio
async def test_html_guide_dryrun_does_not_write(tmp_path, monkeypatch) -> None:
    fake_path = tmp_path / "MACSETUP-USAGE.html"
    monkeypatch.setattr("macsetup.sections.runners.html_guide.GUIDE_PATH", fake_path)

    shell = FakeShell()
    logs: list[str] = []
    executor = make_executor(shell, logs, dry_run=True)
    executor.state.enabled_sections = {"html_guide"}

    ok = await RUNNERS["html_guide"](SECTIONS_BY_SLUG["html_guide"], set(), executor)
    assert ok
    assert not fake_path.exists()
    assert shell.runs == []  # no `open` either
    assert any("[dry-run]" in line for line in logs)
