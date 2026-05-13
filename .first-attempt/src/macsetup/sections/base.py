"""Section ABC. Every installable concern subclasses this.

Each section is responsible for two things:
  - detect(): probe the system, report status + counts (no side effects)
  - install(): run the installs for the items the user ticked

Cross-cutting concerns (sudo, shell, arch, file detection, symlinks) come
from `macsetup.core.*` — sections never reach into each other.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
from typing import Union

from macsetup.core.config import Item


class Status(Enum):
    PENDING = "pending"   # nothing installed
    PARTIAL = "partial"   # some installed
    DONE = "done"         # all installed (or N/A)
    ERROR = "error"       # detection or install failure


@dataclass
class SectionStatus:
    status: Status
    installed: int = 0
    total: int = 0
    message: str = ""


# Async-only log callback. The Section calls emit() to send a line to the
# Progress view (or stdout in headless mode).
Emit = Callable[[str], Awaitable[None]]


class Section(ABC):
    name: str = ""
    icon: str = ""               # Nerd Font glyph; populated in Phase 7
    description: str = ""
    config_file: Union[str, None] = None
    requires_sudo: bool = False

    @abstractmethod
    async def detect(self) -> SectionStatus:
        """Probe the system. Must not modify it."""

    @abstractmethod
    async def install(self, items: list[Item], emit: Emit) -> None:
        """Run installs for the given items, streaming output via emit()."""


class PlaceholderSection(Section):
    """Placeholder for sections not yet implemented.

    Lets us register every section in SECTIONS from day one so the Home
    screen shows the full layout, even before each section's logic exists.
    Phases 5 and 6 replace these with real implementations.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    async def detect(self) -> SectionStatus:
        return SectionStatus(Status.PENDING, 0, 0, "Not yet implemented")

    async def install(self, items: list[Item], emit: Emit) -> None:
        await emit(f"{self.name}: section not yet implemented")
