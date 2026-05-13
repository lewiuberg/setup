import os
from pathlib import Path
from unittest.mock import patch

from macsetup.core import symlink as symlink_mod


def test_link_creates_symlink(tmp_path: Path):
    source = tmp_path / "src.txt"
    source.write_text("hello")
    target = tmp_path / "dst.txt"

    with patch.object(symlink_mod, "BACKUP_ROOT", tmp_path / "backups"):
        result = symlink_mod.link(source, target)

    assert result.action == "linked"
    assert target.is_symlink()
    assert Path(os.readlink(target)).resolve() == source.resolve()


def test_link_skips_when_already_correct(tmp_path: Path):
    source = tmp_path / "src.txt"
    source.write_text("hello")
    target = tmp_path / "dst.txt"
    target.symlink_to(source.resolve())

    with patch.object(symlink_mod, "BACKUP_ROOT", tmp_path / "backups"):
        result = symlink_mod.link(source, target)

    assert result.action == "skipped"
    # No backup directory should have been created.
    assert not (tmp_path / "backups").exists()


def test_link_backs_up_existing_file(tmp_path: Path):
    source = tmp_path / "src.txt"
    source.write_text("new")
    target = tmp_path / "dst.txt"
    target.write_text("old")

    backup_root = tmp_path / "backups"
    with patch.object(symlink_mod, "BACKUP_ROOT", backup_root):
        result = symlink_mod.link(source, target, stamp="20260101T000000Z")

    assert result.action == "backed_up_and_linked"
    assert result.backup_path == backup_root / "20260101T000000Z" / "dst.txt"
    assert result.backup_path is not None
    assert result.backup_path.read_text() == "old"
    assert target.is_symlink()


def test_link_missing_source_raises(tmp_path: Path):
    source = tmp_path / "ghost.txt"
    target = tmp_path / "dst.txt"
    try:
        symlink_mod.link(source, target)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
