"""Dotfile management — symlink from repo into $HOME with backup.

The repo holds canonical dotfiles in `dotfiles/`. This section symlinks
each into $HOME. If a target already exists and differs, it's moved to
~/.macsetup-backups/<timestamp>/ first. Already-correct symlinks are no-ops.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from macsetup.core.config import Item
from macsetup.core.paths import DOTFILES_DIR
from macsetup.core.symlink import link
from macsetup.sections.base import Emit, Section, SectionStatus, Status


@dataclass
class DotfileSpec:
    repo_relative: str          # path under dotfiles/ in the repo
    home_relative: str          # path under $HOME


# Canonical list of dotfiles we manage. The .gitconfig.template is NOT
# symlinked — it's rendered into $HOME/.gitconfig with substituted values
# (deferred to Phase 7 when the user-info modal is wired up).
DOTFILES: list[DotfileSpec] = [
    DotfileSpec("dotfiles/.zshrc", ".zshrc"),
    DotfileSpec("dotfiles/.zprofile", ".zprofile"),
    DotfileSpec("dotfiles/.p10k.zsh", ".p10k.zsh"),
    DotfileSpec("dotfiles/.tmux.conf", ".tmux.conf"),
]


class DotfilesSection(Section):
    name = "Dotfiles"
    description = "Symlink repo dotfiles into $HOME (backs up existing files)"

    def _resolve(self, spec: DotfileSpec) -> tuple[Path, Path]:
        # Source path is repo-relative (DOTFILES_DIR's parent is the repo root).
        source = DOTFILES_DIR.parent / spec.repo_relative
        target = Path.home() / spec.home_relative
        return source, target

    async def detect(self) -> SectionStatus:
        from macsetup.core.detect import is_symlink_to
        ok = 0
        for spec in DOTFILES:
            source, target = self._resolve(spec)
            if is_symlink_to(target, source):
                ok += 1
        total = len(DOTFILES)
        if ok == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if ok == total:
            return SectionStatus(Status.DONE, ok, total)
        return SectionStatus(Status.PARTIAL, ok, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        for spec in DOTFILES:
            source, target = self._resolve(spec)
            if not source.exists():
                await emit(f"skip {spec.home_relative}: source missing at {source}")
                continue
            try:
                result = link(source, target)
            except Exception as e:
                await emit(f"failed {spec.home_relative}: {e}")
                continue
            if result.action == "skipped":
                await emit(f"already linked: ~/{spec.home_relative}")
            elif result.action == "linked":
                await emit(f"linked: ~/{spec.home_relative} → {source}")
            else:
                await emit(
                    f"backed up + linked: ~/{spec.home_relative} → {source} "
                    f"(backup: {result.backup_path})"
                )
