from pathlib import Path

from macsetup.core import detect


def test_path_exists(tmp_path: Path):
    f = tmp_path / "a.txt"
    f.write_text("hello")
    assert detect.path_exists(f)
    assert not detect.path_exists(tmp_path / "missing.txt")


def test_is_symlink_to(tmp_path: Path):
    target = tmp_path / "real.txt"
    target.write_text("x")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    assert detect.is_symlink_to(link, target)
    assert not detect.is_symlink_to(link, tmp_path / "other.txt")
    # Not a symlink at all
    assert not detect.is_symlink_to(target, target)


def test_line_in_file(tmp_path: Path):
    f = tmp_path / "rc"
    f.write_text("alias ll='ls -la'\nexport FOO=1\n")
    assert detect.line_in_file("export FOO=1", f)
    assert detect.line_in_file("alias ll", f)
    assert not detect.line_in_file("nonexistent", f)
    assert not detect.line_in_file("anything", tmp_path / "missing")


def test_line_in_file_handles_binary_gracefully(tmp_path: Path):
    f = tmp_path / "binary"
    f.write_bytes(b"\x00\x01\x02 not text \xff\xfe")
    # Should not raise — bytes that fail decode return False
    detect.line_in_file("anything", f)
