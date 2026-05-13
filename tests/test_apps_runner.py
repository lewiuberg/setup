from __future__ import annotations

import pytest

from macsetup.sections.registry import SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS

from tests.fakes import FakeShell, make_executor


@pytest.mark.asyncio
async def test_raycast_opens_selected_urls() -> None:
    shell = FakeShell()
    logs: list[str] = []
    executor = make_executor(shell, logs)
    section = SECTIONS_BY_SLUG["raycast"]

    # Use the first item from the shipped TOML
    first_item = section.load_items()[0]
    ok = await RUNNERS["raycast"](section, {first_item.name}, executor)
    assert ok
    expected = str(first_item.extras.get("url", ""))
    assert ("open", expected) in shell.runs


@pytest.mark.asyncio
async def test_manual_apps_skips_when_no_selection() -> None:
    shell = FakeShell()
    logs: list[str] = []
    executor = make_executor(shell, logs)

    ok = await RUNNERS["manual_apps"](SECTIONS_BY_SLUG["manual_apps"], set(), executor)
    assert ok
    assert shell.runs == []
    assert any("no manual apps selected" in line for line in logs)


@pytest.mark.asyncio
async def test_raycast_skips_items_without_url() -> None:
    shell = FakeShell()
    logs: list[str] = []
    executor = make_executor(shell, logs)
    section = SECTIONS_BY_SLUG["raycast"]

    # Request an item name not present in the TOML.
    ok = await RUNNERS["raycast"](section, {"NonexistentItem"}, executor)
    assert ok
    assert ("open", "") not in shell.runs
    assert any("no URL in TOML" in line for line in logs)
