"""Safe symlink creation with timestamped backups.

If the target already exists and isn't already a symlink to `source`, move
it to ~/.macsetup-backups/<timestamp>/<filename> before linking. Existing
correct symlinks are no-ops.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Union


BACKUP_ROOT = Path("~/.macsetup-backups").expanduser()


@dataclass
class SymlinkResult:
    action: str  # "skipped" | "linked" | "backed_up_and_linked"
    backup_path: Union[Path, None] = None


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def link(source: Path, target: Path, *, stamp: Union[str, None] = None) -> SymlinkResult:
    """Symlink `target` -> `source`, backing up any existing target."""
    source = source.expanduser().resolve()
    target = target.expanduser()

    if not source.exists():
        raise FileNotFoundError(f"Symlink source does not exist: {source}")

    if target.is_symlink() and Path(os.readlink(target)).resolve() == source:
        return SymlinkResult(action="skipped")

    backup_path: Union[Path, None] = None
    if target.exists() or target.is_symlink():
        stamp = stamp or _utc_stamp()
        backup_dir = BACKUP_ROOT / stamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / target.name
        shutil.move(str(target), str(backup_path))

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source)
    return SymlinkResult(
        action="backed_up_and_linked" if backup_path else "linked",
        backup_path=backup_path,
    )
