"""TOML config loader for the per-section item lists.

All section TOMLs share the same shape:

    [[item]]
    name = "..."
    description = "..."
    required = false
    default = true
    category = "..."     # optional
    # ... any extra keys land in Item.extras

Section-specific keys (url for Raycast, path/mode for secrets, etc.) are
preserved verbatim in Item.extras so each section can pull what it needs
without the loader knowing about every variant.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

import tomlkit


KNOWN_KEYS = {"name", "description", "required", "default", "category"}


@dataclass
class Item:
    name: str
    description: str = ""
    required: bool = False
    default: bool = False
    category: Union[str, None] = None
    extras: dict[str, Any] = field(default_factory=dict)


def load_items(path: Union[str, Path]) -> list[Item]:
    """Load a list of Items from a section TOML file."""
    p = Path(path)
    raw = tomlkit.parse(p.read_text())
    items: list[Item] = []
    for entry in raw.get("item", []):
        name = entry.get("name")
        if not name:
            raise ValueError(f"{p}: each [[item]] must have a name")
        extras = {k: entry[k] for k in entry if k not in KNOWN_KEYS}
        items.append(
            Item(
                name=str(name),
                description=str(entry.get("description", "")),
                required=bool(entry.get("required", False)),
                default=bool(entry.get("default", False)),
                category=str(entry["category"]) if "category" in entry else None,
                extras=extras,
            )
        )
    return items
