"""Repo-relative path constants.

Sections read their config TOMLs and dotfile templates relative to the
repo root, regardless of where the tool was launched from. Resolving via
__file__ keeps this working even after `uv tool install` someday.
"""

from __future__ import annotations

from pathlib import Path


# This file lives at src/macsetup/core/paths.py — four parents up = repo root.
REPO_ROOT: Path = Path(__file__).resolve().parents[3]
CONFIG_DIR: Path = REPO_ROOT / "config"
DOTFILES_DIR: Path = REPO_ROOT / "dotfiles"
ASSETS_DIR: Path = REPO_ROOT / "assets"
