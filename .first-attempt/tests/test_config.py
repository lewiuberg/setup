from pathlib import Path

import pytest

from macsetup.core import config


def test_load_items(tmp_path: Path):
    p = tmp_path / "brews.toml"
    p.write_text(
        """
[[item]]
name = "git"
description = "VCS"
required = true
category = "core"

[[item]]
name = "tmux"
description = "Multiplexer"
default = true
""".strip()
    )
    items = config.load_items(p)
    assert len(items) == 2
    assert items[0].name == "git"
    assert items[0].required is True
    assert items[0].category == "core"
    assert items[0].default is False
    assert items[1].name == "tmux"
    assert items[1].default is True
    assert items[1].category is None


def test_extras_preserved(tmp_path: Path):
    p = tmp_path / "raycast.toml"
    p.write_text(
        """
[[item]]
name = "raycast/github"
url = "https://www.raycast.com/raycast/github"
""".strip()
    )
    items = config.load_items(p)
    assert items[0].extras["url"] == "https://www.raycast.com/raycast/github"


def test_missing_name_raises(tmp_path: Path):
    p = tmp_path / "bad.toml"
    p.write_text(
        """
[[item]]
description = "no name"
""".strip()
    )
    with pytest.raises(ValueError):
        config.load_items(p)


def test_empty_file_returns_no_items(tmp_path: Path):
    p = tmp_path / "empty.toml"
    p.write_text("")
    assert config.load_items(p) == []
