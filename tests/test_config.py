from pathlib import Path

import pytest

from macsetup.core.config import CONFIG_DIR, ConfigError, Item, load_items, load_section


def test_load_items_parses_brews(tmp_path: Path) -> None:
    toml = tmp_path / "brews.toml"
    toml.write_text(
        """
        [[item]]
        name = "git"
        description = "Distributed VCS"

        [[item]]
        name = "poetry"
        description = "Legacy Python dependency manager"
        default = false
        """,
        encoding="utf-8",
    )
    items = load_items(toml)
    assert items == [
        Item(name="git", description="Distributed VCS", default=True, extras={}),
        Item(
            name="poetry",
            description="Legacy Python dependency manager",
            default=False,
            extras={},
        ),
    ]


def test_load_items_captures_extras(tmp_path: Path) -> None:
    toml = tmp_path / "mise.toml"
    toml.write_text(
        """
        [[item]]
        name = "python"
        version = "3.12"
        """,
        encoding="utf-8",
    )
    items = load_items(toml)
    assert items[0].name == "python"
    assert items[0].extras == {"version": "3.12"}


def test_load_items_rejects_missing_name(tmp_path: Path) -> None:
    toml = tmp_path / "bad.toml"
    toml.write_text("[[item]]\ndescription = \"no name\"\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="missing `name`"):
        load_items(toml)


def test_load_items_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_items(tmp_path / "nope.toml")


def test_shipped_brews_config_parses() -> None:
    items = load_section("brews", CONFIG_DIR)
    names = [item.name for item in items]
    assert "git" in names
    assert "mise" in names
    assert "uv" in names
