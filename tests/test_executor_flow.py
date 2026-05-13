"""Tests for the embedded executor flow in PlanScreen."""
from __future__ import annotations

import pytest

from macsetup.app import MacsetupApp
from macsetup.screens.plan import PlanScreen, SectionRow
from macsetup.sections.registry import ALL_SECTIONS, SECTIONS_BY_SLUG
from macsetup.sections.runners import RUNNERS, register_runner
from macsetup.state import PlanState


@pytest.mark.asyncio
async def test_run_plan_executes_at_least_one_runner() -> None:
    """Pressing `r` switches to running mode and the homebrew runner produces output."""
    app = MacsetupApp(dry_run=True)
    async with app.run_test() as pilot:
        await pilot.pause()
        plan = app.screen
        assert isinstance(plan, PlanScreen)
        # Limit to homebrew to keep the test fast.
        plan.state.enabled_sections = {"homebrew"}
        await pilot.press("r")
        # Give the loop a few ticks to run + emit the summary.
        for _ in range(8):
            await pilot.pause()
        assert plan._executing is True
        assert plan.state.section_status.get("homebrew") in {"ok", "skipped", "failed"}


@pytest.mark.asyncio
async def test_runner_registry_dispatches_by_slug() -> None:
    """register_runner stores into a slug-keyed dict."""
    sentinel: list[str] = []

    @register_runner("__test_section__")
    async def _runner(section, items, executor):
        sentinel.append(section.slug)
        return True

    assert "__test_section__" in RUNNERS
    runner = RUNNERS["__test_section__"]

    class _FakeSection:
        slug = "__test_section__"
        display_name = "Test"
        items_config = None
        interactive = False

    class _FakeExecutor:
        def log(self, _msg): ...

    ok = await runner(_FakeSection(), set(), _FakeExecutor())  # type: ignore[arg-type]
    assert ok is True
    assert sentinel == ["__test_section__"]
    RUNNERS.pop("__test_section__", None)


def test_homebrew_runner_registered() -> None:
    assert "homebrew" in RUNNERS
    assert SECTIONS_BY_SLUG["homebrew"].display_name == "Homebrew"


@pytest.mark.asyncio
async def test_section_row_renders_status_glyph_during_run() -> None:
    """When section_status is set, the row's leading glyph reflects status."""
    state = PlanState.initial(ALL_SECTIONS)
    row = SectionRow(SECTIONS_BY_SLUG["homebrew"], state)
    # Pre-run: shows the enabled glyph (✓).
    assert "✓" in row._render_label().plain
    # During run.
    state.section_status["homebrew"] = "running"
    assert "▶" in row._render_label().plain
    # Done.
    state.section_status["homebrew"] = "ok"
    assert "✓" in row._render_label().plain
    # Failure.
    state.section_status["homebrew"] = "failed"
    assert "✗" in row._render_label().plain
