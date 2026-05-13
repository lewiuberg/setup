"""Dotfile generation: backup existing files and render new ones from Jinja2.

The dotfile section of the wizard uses these helpers. Each generated file gets
the full template context (which sections are enabled, which items selected)
so optional blocks render conditionally.
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )


@dataclass(frozen=True)
class DotfileTarget:
    template: str
    dest: Path


def render(template_name: str, context: Mapping[str, object]) -> str:
    return _env().get_template(template_name).render(**context)


def backup_existing(paths: list[Path], home: Path | None = None) -> Path | None:
    """Move any existing paths into a timestamped backup directory under $HOME.

    Returns the backup directory (None if nothing was moved).
    """
    home = home or Path.home()
    existing = [p for p in paths if p.exists()]
    if not existing:
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = home / ".dotfile-backups" / ts
    backup_dir.mkdir(parents=True, exist_ok=True)
    for path in existing:
        shutil.move(str(path), str(backup_dir / path.name))
    return backup_dir


def write(content: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
