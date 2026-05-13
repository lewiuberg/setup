from __future__ import annotations

import pytest

from macsetup.core.shell import CommandResult
from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


@pytest.mark.asyncio
async def test_github_auth_skips_when_already_authenticated() -> None:
    shell = FakeShell(installed={"gh"})
    shell.canned[("gh", "auth", "status")] = CommandResult(0, "Logged in")
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["github_auth"](SECTIONS_BY_SLUG["github_auth"], set(), executor)
    assert ok
    assert any("already authenticated" in line for line in logs)


@pytest.mark.asyncio
async def test_github_auth_fails_when_gh_missing() -> None:
    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["github_auth"](SECTIONS_BY_SLUG["github_auth"], set(), executor)
    assert ok is False
    assert any("gh CLI not installed" in line for line in logs)


@pytest.mark.asyncio
async def test_azure_devops_copies_existing_key_and_opens_url(
    tmp_path, monkeypatch
) -> None:
    fake_home = tmp_path
    ssh_dir = fake_home / ".ssh"
    ssh_dir.mkdir()
    pubkey = ssh_dir / "id_ed25519.pub"
    pubkey.write_text("ssh-ed25519 AAAAC3 user@example.com")
    monkeypatch.setattr(
        "macsetup.sections.runners.auth.SSH_KEY_CANDIDATES",
        (pubkey,),
    )

    shell = FakeShell(installed=set())
    logs: list[str] = []
    executor = make_executor(shell, logs)
    ok = await RUNNERS["azure_devops"](SECTIONS_BY_SLUG["azure_devops"], set(), executor)
    assert ok
    assert any(cmd[0] == "open" for cmd in shell.runs)
    assert any("copied to clipboard" in line or "copy manually" in line for line in logs)
