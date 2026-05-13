from __future__ import annotations

import asyncio
import os
import shutil
from dataclasses import dataclass
from typing import Awaitable, Callable, Iterable, Sequence


@dataclass(frozen=True)
class CommandResult:
    exit_code: int
    output: str

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


class Shell:
    """Thin async wrapper around subprocess for the wizard.

    All methods return capturable results. Use `stream` when you want each
    line piped to a callback (so the TUI log can update live).
    """

    def which(self, name: str) -> str | None:
        return shutil.which(name)

    def has(self, name: str) -> bool:
        return self.which(name) is not None

    async def run(
        self,
        cmd: Sequence[str],
        *,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        input_: str | None = None,
    ) -> CommandResult:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            stdin=asyncio.subprocess.PIPE if input_ is not None else None,
            env={**os.environ, **(env or {})},
            cwd=cwd,
        )
        stdout, _ = await proc.communicate(input_.encode() if input_ else None)
        return CommandResult(
            exit_code=proc.returncode or 0,
            output=stdout.decode(errors="replace"),
        )

    async def stream(
        self,
        cmd: Sequence[str],
        on_line: Callable[[str], Awaitable[None] | None],
        *,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
    ) -> int:
        """Run `cmd`, fire `on_line` for each stdout/stderr line. Returns exit code."""
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env={**os.environ, **(env or {})},
            cwd=cwd,
        )
        assert proc.stdout is not None
        async for raw in proc.stdout:
            line = raw.decode(errors="replace").rstrip("\n")
            result = on_line(line)
            if asyncio.iscoroutine(result):
                await result
        await proc.wait()
        return proc.returncode or 0

    async def has_all(self, names: Iterable[str]) -> bool:
        return all(self.has(n) for n in names)
