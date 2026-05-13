"""Sanity tests for the section registry and the Section ABC.

Real install logic is exercised on the live machine (no good way to mock
brew/code without a fragile integration shim). These tests just confirm:
  - every section has a non-empty name
  - the registry is ordered as we expect
  - PlaceholderSection's detect() doesn't crash
  - imports work
"""

from __future__ import annotations

from macsetup.sections import SECTIONS
from macsetup.sections.base import (
    PlaceholderSection,
    Section,
    SectionStatus,
    Status,
)


def test_every_section_has_a_name():
    for section in SECTIONS:
        assert section.name, f"{type(section).__name__} has empty name"


def test_section_names_are_unique():
    names = [s.name for s in SECTIONS]
    assert len(names) == len(set(names)), f"Duplicate section names: {names}"


def test_registry_order_starts_with_rosetta_homebrew():
    assert SECTIONS[0].name == "Rosetta"
    assert SECTIONS[1].name == "Homebrew"


def test_all_sections_are_section_subclasses():
    for s in SECTIONS:
        assert isinstance(s, Section)


async def test_placeholder_detect_returns_pending():
    p = PlaceholderSection("Test")
    status = await p.detect()
    assert status.status is Status.PENDING
    assert "Not yet implemented" in status.message


async def test_placeholder_install_emits_message():
    p = PlaceholderSection("Test")
    captured: list[str] = []

    async def emit(line: str) -> None:
        captured.append(line)

    await p.install([], emit)
    assert any("Test" in line for line in captured)


def test_section_status_default_fields():
    s = SectionStatus(Status.PENDING)
    assert s.installed == 0
    assert s.total == 0
    assert s.message == ""
