"""Custom widgets — section row, progress bar, status pill."""

from __future__ import annotations

from macsetup.sections.base import SectionStatus, Status


# 10-cell ASCII progress bar — full / partial / empty / hatched (error).
BAR_WIDTH = 10
FILLED = "█"
EMPTY = "░"
ERROR = "╳"


def render_bar(status: SectionStatus) -> str:
    """Render a 10-cell progress bar reflecting installed/total."""
    if status.status is Status.ERROR:
        return ERROR * BAR_WIDTH
    if status.total == 0:
        # Sections without per-item totals (Rosetta, Homebrew, etc.):
        # full when done, empty otherwise.
        return FILLED * BAR_WIDTH if status.status is Status.DONE else EMPTY * BAR_WIDTH
    filled = round(BAR_WIDTH * status.installed / status.total)
    return FILLED * filled + EMPTY * (BAR_WIDTH - filled)


# Status → Rich markup colour. Matches VS Code Default Dark+ semantic colours.
STATUS_COLOUR: dict[Status, str] = {
    Status.PENDING: "#6a9955",   # comment grey — neutral
    Status.PARTIAL: "#dcdcaa",   # warning yellow
    Status.DONE: "#6a9955",      # success green
    Status.ERROR: "#f44747",     # error red
}


def render_row(icon: str, name: str, status: SectionStatus) -> str:
    """Single-line Rich-markup string for a Home row.

    Layout: `<icon>  <name padded>  <bar>  <fraction or message>`
    """
    bar = render_bar(status)
    colour = STATUS_COLOUR[status.status]
    if status.total > 0:
        right = f"{status.installed:>2}/{status.total:<3}"
    elif status.message:
        right = status.message
    else:
        right = "done" if status.status is Status.DONE else "pending"
    return (
        f"  [{colour}]{icon}[/]  "
        f"[bold]{name:<22}[/]  "
        f"[{colour}]{bar}[/]  "
        f"[{colour}]{right}[/]"
    )
