"""Reusable test doubles for runner tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable, Sequence

from macsetup.core.executor import Executor
from macsetup.core.shell import CommandResult
from macsetup.core.sudo import SudoKeepalive
from macsetup.state import PlanState


@dataclass
class FakeShell:
    """A Shell stand-in. Looks up canned results by the first arg of the cmd."""

    canned: dict[tuple[str, ...], CommandResult] = field(default_factory=dict)
    installed: set[str] = field(default_factory=set)
    runs: list[tuple[str, ...]] = field(default_factory=list)
    streams: list[tuple[str, ...]] = field(default_factory=list)
    stream_exit_code: int = 0

    def which(self, name: str) -> str | None:
        return f"/fake/bin/{name}" if name in self.installed else None

    def has(self, name: str) -> bool:
        return name in self.installed

    async def run(self, cmd: Sequence[str], **_: object) -> CommandResult:
        key = tuple(cmd)
        self.runs.append(key)
        if key in self.canned:
            return self.canned[key]
        # Fallback: pretend success with empty output.
        return CommandResult(exit_code=0, output="")

    async def stream(
        self,
        cmd: Sequence[str],
        on_line: Callable[[str], Awaitable[None] | None],
        **_: object,
    ) -> int:
        self.streams.append(tuple(cmd))
        return self.stream_exit_code


def make_executor(
    shell: FakeShell,
    log_sink: list[str] | None = None,
    *,
    dry_run: bool = False,
) -> Executor:
    sink = log_sink if log_sink is not None else []
    return Executor(
        shell=shell,  # type: ignore[arg-type]
        log=sink.append,
        progress=lambda msg: None,
        suspend=lambda: _NoOpSuspend(),
        ensure_sudo=_always_true,
        state=PlanState(),
        keepalive=SudoKeepalive(),
        dry_run=dry_run,
    )


class _NoOpSuspend:
    def __enter__(self): return self
    def __exit__(self, *args): return False


async def _always_true() -> bool:
    return True
