from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


@dataclass(frozen=True)
class Item:
    """A single selectable item in a section (brew formula, cask, extension, …)."""

    name: str
    description: str = ""
    default: bool = True
    extras: dict[str, object] = field(default_factory=dict)


class ConfigError(ValueError):
    pass


def load_items(path: Path) -> list[Item]:
    """Parse a TOML file with `[[item]]` entries into a list of Item objects."""
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    raw_items = data.get("item", [])
    if not isinstance(raw_items, list):
        raise ConfigError(f"{path}: expected `[[item]]` entries, got {type(raw_items).__name__}")

    items: list[Item] = []
    for index, entry in enumerate(raw_items):
        if not isinstance(entry, dict):
            raise ConfigError(f"{path}: item #{index} is not a table")
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ConfigError(f"{path}: item #{index} missing `name`")
        description = entry.get("description", "")
        default = bool(entry.get("default", True))
        extras = {k: v for k, v in entry.items() if k not in {"name", "description", "default"}}
        items.append(Item(name=name, description=description, default=default, extras=extras))

    return items


def load_section(section: str, config_dir: Path = CONFIG_DIR) -> list[Item]:
    """Convenience: load `<config_dir>/<section>.toml`."""
    return load_items(config_dir / f"{section}.toml")
