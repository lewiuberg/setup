"""Runners for GitHub and Azure DevOps authentication.

GitHub uses `gh auth login` (interactive — yields the TTY). Azure DevOps has
no equivalent single-command flow, so we generate/locate an SSH key, copy the
public half to the clipboard, and open the DevOps SSH-keys page in the browser.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner

SSH_KEY_CANDIDATES = (
    Path.home() / ".ssh" / "id_ed25519.pub",
    Path.home() / ".ssh" / "id_rsa.pub",
)
AZURE_DEVOPS_URL = "https://dev.azure.com"


# ---------------------------------------------------------------------------
# GitHub
# ---------------------------------------------------------------------------

@register_runner("github_auth")
async def run_github_auth(section: Section, items: set[str], executor: Executor) -> bool:
    if not executor.shell.has("gh"):
        executor.log("  [#f44747]gh CLI not installed (add `gh` to brews.toml first)[/]")
        return False

    status = await executor.shell.run(["gh", "auth", "status"])
    if status.ok:
        executor.log(f"  [#4ec9b0]✓[/] already authenticated to GitHub")
        return True

    if executor.dry_run:
        executor.log("  [#ce9178][dry-run][/] would launch `gh auth login` interactively")
        return True

    executor.log("  launching `gh auth login` — generates SSH key, uploads it, configures credential helper…")
    with executor.suspend():
        proc = subprocess.run(["gh", "auth", "login"], check=False)
    if proc.returncode != 0:
        executor.log(f"  [#ce9178]gh auth login exited {proc.returncode}[/]")
        return False
    executor.log(f"  [#4ec9b0]✓[/] GitHub auth complete")
    return True


# ---------------------------------------------------------------------------
# Azure DevOps
# ---------------------------------------------------------------------------

def _find_ssh_pubkey() -> Path | None:
    for candidate in SSH_KEY_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


@register_runner("azure_devops")
async def run_azure_devops(section: Section, items: set[str], executor: Executor) -> bool:
    pubkey = _find_ssh_pubkey()
    if pubkey is None:
        if executor.dry_run:
            executor.log("  [#ce9178][dry-run][/] would run `ssh-keygen -t ed25519` to create a keypair")
            return True
        executor.log("  no SSH public key found — generating ed25519 keypair…")
        # ssh-keygen is interactive (passphrase). Yield the TTY.
        with executor.suspend():
            proc = subprocess.run(
                ["ssh-keygen", "-t", "ed25519", "-f", str(Path.home() / ".ssh" / "id_ed25519")],
                check=False,
            )
        if proc.returncode != 0:
            executor.log(f"  [#f44747]ssh-keygen exited {proc.returncode}[/]")
            return False
        pubkey = Path.home() / ".ssh" / "id_ed25519.pub"

    pubkey_text = pubkey.read_text()
    copy = await executor.shell.run(["sh", "-c", f"printf '%s' '{pubkey_text}' | pbcopy"])
    if not copy.ok:
        executor.log("  [#ce9178]pbcopy failed (clipboard not available); print below to copy manually[/]")
        executor.log(f"\n{pubkey_text}\n")
    else:
        executor.log(f"  [#4ec9b0]✓[/] SSH public key ({pubkey.name}) copied to clipboard")

    await executor.shell.run(["open", AZURE_DEVOPS_URL])
    executor.log(
        "  → opened dev.azure.com — sign in, then: "
        "User Settings (top right) → SSH public keys → Add → paste"
    )
    return True
