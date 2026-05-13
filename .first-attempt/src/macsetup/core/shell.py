"""Async subprocess wrapper.

Streams stdout/stderr line-by-line to a callback (for the live log view)
while also capturing full output for inspection. The single entry point
for every external command the sections run.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Union


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


LogCallback = Union[Callable[[str], None], Callable[[str], Awaitable[None]]]


async def run(
    cmd: Sequence[str],
    *,
    cwd: Union[str, os.PathLike[str], None] = None,
    env: Union[dict[str, str], None] = None,
    on_line: Union[LogCallback, None] = None,
    input: Union[str, None] = None,
) -> CommandResult:
    """Run a command asynchronously, streaming output to `on_line`."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE if input is not None else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,
    )

    if input is not None and proc.stdin is not None:
        proc.stdin.write(input.encode())
        await proc.stdin.drain()
        proc.stdin.close()

    stdout_buf: list[str] = []
    stderr_buf: list[str] = []

    async def _drain(stream: asyncio.StreamReader, buf: list[str]) -> None:
        async for raw in stream:
            line = raw.decode(errors="replace").rstrip("\n")
            buf.append(line)
            if on_line is not None:
                outcome = on_line(line)
                if asyncio.iscoroutine(outcome):
                    await outcome

    assert proc.stdout is not None and proc.stderr is not None
    await asyncio.gather(
        _drain(proc.stdout, stdout_buf),
        _drain(proc.stderr, stderr_buf),
    )
    returncode = await proc.wait()
    return CommandResult(
        returncode=returncode,
        stdout="\n".join(stdout_buf),
        stderr="\n".join(stderr_buf),
    )


async def run_capture(cmd: Sequence[str], **kwargs) -> CommandResult:
    """Convenience: like run() but discards live streaming."""
    kwargs.pop("on_line", None)
    return await run(cmd, **kwargs)
