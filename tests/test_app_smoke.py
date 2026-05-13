"""Headless smoke test: the app boots, the plan screen mounts, no errors raised."""
from __future__ import annotations

import pytest

from macsetup.app import MacsetupApp
from macsetup.screens.plan import PlanScreen


@pytest.mark.asyncio
async def test_app_boots_into_plan_screen() -> None:
    app = MacsetupApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, PlanScreen)
        list_view = app.screen.query_one("#section-list")
        assert list_view is not None
        # First section should be highlighted on mount.
        assert list_view.highlighted_child is not None


@pytest.mark.asyncio
async def test_toggle_section_changes_state() -> None:
    app = MacsetupApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        screen: PlanScreen = app.screen  # type: ignore[assignment]
        first_slug = screen._current_row().section.slug  # type: ignore[union-attr]
        assert screen.state.is_section_enabled(first_slug)
        await pilot.press("enter")
        await pilot.pause()
        assert not screen.state.is_section_enabled(first_slug)
        await pilot.press("enter")
        await pilot.pause()
        assert screen.state.is_section_enabled(first_slug)


@pytest.mark.asyncio
async def test_select_none_clears_items() -> None:
    app = MacsetupApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        screen: PlanScreen = app.screen  # type: ignore[assignment]
        # Navigate down to the Brews section (index 3 in the registry).
        for _ in range(3):
            await pilot.press("down")
        await pilot.pause()
        row = screen._current_row()
        assert row is not None
        assert row.section.slug == "brews"
        assert screen.state.selected_count("brews") > 0
        await pilot.press("n")
        await pilot.pause()
        assert screen.state.selected_count("brews") == 0
