from __future__ import annotations

import pytest

from macsetup.app import MacsetupApp
from macsetup.core.dryrun import DryRunShell
from macsetup.core.shell import Shell
from macsetup.screens.plan import PlanScreen
from macsetup.sections.registry import ALL_SECTIONS
from macsetup.state import PlanState


@pytest.mark.asyncio
async def test_dryrun_shell_short_circuits_run() -> None:
    captured: list[str] = []
    dry = DryRunShell(Shell(), captured.append)
    result = await dry.run(["rm", "-rf", "/dangerous"])
    assert result.ok
    assert result.output == ""
    assert any("would run" in line for line in captured)
    assert any("rm -rf /dangerous" in line for line in captured)


@pytest.mark.asyncio
async def test_dryrun_shell_short_circuits_stream() -> None:
    captured: list[str] = []
    dry = DryRunShell(Shell(), captured.append)
    code = await dry.stream(["brew", "install", "git"], lambda _line: None)
    assert code == 0
    assert any("would stream" in line for line in captured)


@pytest.mark.asyncio
async def test_run_plan_marks_disabled_sections_as_skipped() -> None:
    app = MacsetupApp(dry_run=True)
    async with app.run_test() as pilot:
        await pilot.pause()
        plan: PlanScreen = app.screen  # type: ignore[assignment]
        # Disable everything so the loop just marks everything skipped.
        plan.state.enabled_sections = set()
        await pilot.press("r")
        for _ in range(6):
            await pilot.pause()
        for section in ALL_SECTIONS:
            assert plan.state.section_status.get(section.slug) == "skipped"


@pytest.mark.asyncio
async def test_run_plan_finishes_and_marks_executing() -> None:
    """After `r` completes, every section has a status and the executing flag
    stays set so re-presses are ignored."""
    app = MacsetupApp(dry_run=True)
    async with app.run_test() as pilot:
        await pilot.pause()
        plan: PlanScreen = app.screen  # type: ignore[assignment]
        plan.state.enabled_sections = set()  # all skipped — finishes fast
        await pilot.press("r")
        for _ in range(6):
            await pilot.pause()
        assert plan._executing is True
        # Every section got a status update (skipped, since none enabled).
        slugs = {s.slug for s in ALL_SECTIONS}
        assert set(plan.state.section_status.keys()) == slugs


def test_main_accepts_dry_run_flag(monkeypatch) -> None:
    """CLI parses `--dry-run` and constructs the app with the flag."""
    import sys

    captured: dict[str, bool] = {}

    def fake_run(self):
        captured["dry_run"] = self.dry_run

    monkeypatch.setattr(MacsetupApp, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["macsetup", "--dry-run"])

    from macsetup.__main__ import main
    main()
    assert captured["dry_run"] is True
