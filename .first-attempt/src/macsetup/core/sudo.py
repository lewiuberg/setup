"""One-shot sudo password prompt with background keep-alive.

Collect the password once via the TUI's sudo modal, validate it with
`sudo -S -v`, then run a background task that hits `sudo -n -v` every
60 seconds so subsequent sections don't re-prompt.

The password is held only as a local string for the lifetime of the
validation call; never written to disk or environment.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from macsetup.core.shell import run

# macOS default sudo timeout is 5 minutes. Refresh every minute to leave
# headroom for brief sleeps and slow steps.
KEEPALIVE_INTERVAL = 60.0


class SudoError(Exception):
    """Raised when sudo validation fails."""


async def validate(password: str) -> None:
    """Validate by running `sudo -S -v`. Raises SudoError on failure."""
    result = await run(["sudo", "-S", "-v"], input=password + "\n")
    if not result.ok:
        raise SudoError(result.stderr.strip() or "sudo validation failed")


async def is_cached() -> bool:
    """True iff sudo can run without prompting (credential still fresh)."""
    return (await run(["sudo", "-n", "-v"])).ok


@asynccontextmanager
async def keepalive() -> AsyncIterator[None]:
    """Background task that refreshes the sudo timestamp.

    Usage:
        async with keepalive():
            # any sudo-using code in here gets unattended sudo
            ...
    """
    stop = asyncio.Event()

    async def _loop() -> None:
        while not stop.is_set():
            try:
                await asyncio.wait_for(stop.wait(), timeout=KEEPALIVE_INTERVAL)
                return
            except asyncio.TimeoutError:
                await run(["sudo", "-n", "-v"])

    task = asyncio.create_task(_loop())
    try:
        yield
    finally:
        stop.set()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
