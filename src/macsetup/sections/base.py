from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from macsetup.core.config import Item, load_section


@dataclass(frozen=True)
class Section:
    """A single section in the wizard plan.

    `items_config` is the stem of a `config/<name>.toml` file; if set, this
    section has per-item selection. Sections without `items_config` are
    singletons (install / configure / skip).

    `interactive` flags sections that need to yield the TTY to a subprocess
    (p10k configure, gh auth login, …). The executor uses this to show a
    modal before running.
    """

    slug: str
    display_name: str
    description: str
    items_config: str | None = None
    interactive: bool = False

    def load_items(self) -> list[Item]:
        if self.items_config is None:
            return []
        return _cached_items(self.items_config)


# Module-level cache so we don't hit disk every time the plan screen re-renders.
_ITEMS_CACHE: dict[str, list[Item]] = {}


def _cached_items(name: str) -> list[Item]:
    cached = _ITEMS_CACHE.get(name)
    if cached is None:
        cached = load_section(name)
        _ITEMS_CACHE[name] = cached
    return cached


def clear_items_cache() -> None:
    _ITEMS_CACHE.clear()
