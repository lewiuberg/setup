from __future__ import annotations

from pathlib import Path

import pytest

from macsetup.core.dotfiles import backup_existing, render, write


def test_render_zshrc_includes_mise_block_when_flagged() -> None:
    out = render("zshrc.j2", {
        "include_mise": True,
        "include_poetry": False,
        "include_uv": True,
        "extra_plugins": [],
    })
    assert 'eval "$(mise activate zsh)"' in out
    assert "Poetry (legacy projects)" not in out
    assert "uv (Python project manager)" in out


def test_render_zshrc_omits_optional_blocks() -> None:
    out = render("zshrc.j2", {
        "include_mise": False,
        "include_poetry": False,
        "include_uv": False,
        "extra_plugins": [],
    })
    assert "mise activate zsh" not in out
    assert "Poetry (legacy projects)" not in out


def test_render_warprc_emits_one_line_per_shortcut() -> None:
    out = render("warprc.j2", {"shortcuts": [("dev", "~/code"), ("home", "~")]})
    assert out.splitlines() == ["dev:~/code", "home:~"]


def test_render_zshrc_appends_extra_plugins() -> None:
    out = render("zshrc.j2", {
        "include_mise": False,
        "include_poetry": True,
        "include_uv": False,
        "extra_plugins": ["poetry"],
    })
    # plugins=( ... poetry ) somewhere in the file
    plugins_line = [
        line for line in out.splitlines() if line.startswith("plugins=")
    ]
    assert plugins_line
    assert "poetry" in plugins_line[0]


def test_backup_existing_moves_files(tmp_path: Path) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    zshrc = fake_home / ".zshrc"
    warprc = fake_home / ".warprc"
    zshrc.write_text("old zshrc")
    warprc.write_text("old warprc")
    untouched = fake_home / ".zprofile"

    backup_dir = backup_existing([zshrc, warprc, untouched], home=fake_home)
    assert backup_dir is not None
    assert (backup_dir / ".zshrc").read_text() == "old zshrc"
    assert (backup_dir / ".warprc").read_text() == "old warprc"
    assert not zshrc.exists()
    assert not warprc.exists()


def test_backup_existing_returns_none_when_no_files(tmp_path: Path) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    result = backup_existing([fake_home / ".zshrc"], home=fake_home)
    assert result is None


def test_write_creates_parent_dirs(tmp_path: Path) -> None:
    target = tmp_path / "deep" / "tree" / "file.txt"
    write("hello", target)
    assert target.read_text() == "hello"
