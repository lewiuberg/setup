"""SSH / GPG key restoration.

The repo never contains key material. This section detects which expected
keys are present, fixes permissions, and (in Phase 7) prompts the user
for a backup source when keys are missing. For now, install() will report
missing keys but not auto-restore — that needs the source-prompt modal.
"""

from __future__ import annotations

import os
from pathlib import Path

from macsetup.core.config import Item, load_items
from macsetup.core.detect import command_exists
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


def _expand(path: str) -> Path:
    return Path(path).expanduser()


class SecretsSection(Section):
    name = "Secrets"
    description = "SSH / GPG key restore (no key material in repo)"
    config_file = "secrets.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        present = sum(1 for item in items if _expand(item.extras["path"]).exists())
        total = len(items)
        if present == 0:
            return SectionStatus(Status.PENDING, 0, total, "No keys present")
        if present == total:
            return SectionStatus(Status.DONE, present, total)
        return SectionStatus(Status.PARTIAL, present, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        await emit(
            "Restoring keys requires a backup source (path / mounted volume / "
            "1Password CLI). The source-prompt modal is Phase 7 work; "
            "for now, restore the files manually then re-run to verify permissions."
        )
        await emit("")
        await emit("Expected files:")
        for item in items:
            path = _expand(item.extras["path"])
            mark = "✓" if path.exists() else "✗"
            mode = item.extras.get("mode", "")
            mode_str = f" [{mode}]" if mode else ""
            await emit(f"  {mark}  {path}{mode_str}  — {item.description}")
        await emit("")

        await self._fix_permissions(items, emit)
        await self._configure_git_signing(emit)
        await self._add_ssh_key_to_keychain(items, emit)

    async def _fix_permissions(self, items: list[Item], emit: Emit) -> None:
        # Ensure parent directories (~/.ssh, ~/.gnupg) have 0700.
        for top in (Path.home() / ".ssh", Path.home() / ".gnupg"):
            if top.exists():
                os.chmod(top, 0o700)
        for item in items:
            path = _expand(item.extras["path"])
            mode_str = item.extras.get("mode")
            if not path.exists() or not mode_str:
                continue
            try:
                os.chmod(path, int(str(mode_str), 8))
                await emit(f"chmod {mode_str} {path}")
            except OSError as e:
                await emit(f"chmod failed on {path}: {e}")

    async def _configure_git_signing(self, emit: Emit) -> None:
        import tomlkit
        raw = tomlkit.parse((CONFIG_DIR / "secrets.toml").read_text())
        signing = raw.get("git-signing", {})
        if not signing.get("enable"):
            return
        if not command_exists("gpg"):
            await emit("GPG not installed — skipping git signing config")
            return
        await emit("Configuring git commit signing…")
        await run(
            ["git", "config", "--global", "commit.gpgsign", "true"],
            on_line=emit,
        )
        which_gpg = await run(["which", "gpg"])
        if which_gpg.ok:
            gpg_path = which_gpg.stdout.strip()
            await run(
                ["git", "config", "--global", "gpg.program", gpg_path],
                on_line=emit,
            )

    async def _add_ssh_key_to_keychain(self, items: list[Item], emit: Emit) -> None:
        for item in items:
            if not item.extras.get("add_to_keychain"):
                continue
            path = _expand(item.extras["path"])
            if not path.exists():
                continue
            await emit(f"ssh-add --apple-use-keychain {path}")
            await run(["ssh-add", "--apple-use-keychain", str(path)], on_line=emit)
