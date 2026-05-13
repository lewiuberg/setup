from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from macsetup.sections.base import Section


@dataclass
class PlanState:
    """User's choices in the plan phase plus per-section run status.

    `enabled_sections` is the set of section slugs that will run.
    `enabled_items[slug]` is the set of item names selected within that section.
    `section_status[slug]` is `"running" | "ok" | "failed" | "skipped"` while
    the executor is iterating; absent before the run starts.
    """

    enabled_sections: set[str] = field(default_factory=set)
    enabled_items: dict[str, set[str]] = field(default_factory=dict)
    section_status: dict[str, str] = field(default_factory=dict)

    @classmethod
    def initial(cls, sections: Iterable[Section]) -> "PlanState":
        state = cls()
        for section in sections:
            state.enabled_sections.add(section.slug)
            if section.items_config is None:
                continue
            items = section.load_items()
            state.enabled_items[section.slug] = {i.name for i in items if i.default}
        return state

    def is_section_enabled(self, slug: str) -> bool:
        return slug in self.enabled_sections

    def toggle_section(self, slug: str) -> None:
        if slug in self.enabled_sections:
            self.enabled_sections.discard(slug)
        else:
            self.enabled_sections.add(slug)

    def selected_count(self, slug: str) -> int:
        return len(self.enabled_items.get(slug, set()))

    def set_items(self, slug: str, names: Iterable[str]) -> None:
        self.enabled_items[slug] = set(names)
