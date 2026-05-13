"""Dry-run wrapper around `Shell` — logs commands without executing them.

The wrapper short-circuits `run` and `stream` to return success with no side
effects. `which`/`has` still hit the real binary tree so detection logic gives
realistic answers. Dotfile writes are NOT mocked here; the dotfiles runner
checks `executor.dry_run` directly if it needs to skip file writes.
"""
from __future__ import annotations

from typing import Awaitable, Callable, Sequence

from macsetup.core.shell import CommandResult, Shell

LogFn = Callable[[str], None]


class DryRunShell:
    def __init__(self, real: Shell, log: LogFn) -> None:
        self._real = real
        self._log = log

    def which(self, name: str) -> str | None:
        return self._real.which(name)

    def has(self, name: str) -> bool:
        return self._real.has(name)

    async def run(self, cmd: Sequence[str], **_: object) -> CommandResult:
        self._log(f"  [#ce9178][dry-run][/] would run: {' '.join(cmd)}")
        return CommandResult(exit_code=0, output="")

    async def stream(
        self,
        cmd: Sequence[str],
        on_line: Callable[[str], Awaitable[None] | None],
        **_: object,
    ) -> int:
        self._log(f"  [#ce9178][dry-run][/] would stream: {' '.join(cmd)}")
        return 0
