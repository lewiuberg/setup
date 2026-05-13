from __future__ import annotations

import asyncio
import subprocess
from contextlib import AbstractContextManager
from typing import Callable

YieldTTY = Callable[[], AbstractContextManager[None]]

_OSASCRIPT_PROMPT = (
    'text returned of (display dialog '
    '"macsetup needs your administrator password to install App Store apps '
    'and other system tools.\\n\\nIt will only be used to refresh the sudo '
    'timestamp for this run." '
    'default answer "" with hidden answer '
    'with title "macsetup — administrator password" '
    'with icon caution)'
)


class SudoKeepalive:
    """Background task that refreshes the sudo timestamp every `interval` seconds.

    Pattern mirrors the legacy `install.sh` keep-alive loop: once the user has
    typed their password once via `sudo -v`, this task pings `sudo -n true`
    periodically so subsequent sudo calls never re-prompt.
    """

    def __init__(self, interval: int = 60) -> None:
        self.interval = interval
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is not None and not self._task.done():
            return
        self._task = asyncio.create_task(self._loop())

    def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            self._task = None

    async def _loop(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.interval)
                # Non-interactive refresh; if it fails (timestamp expired) we
                # silently give up — the next sudo call will reprompt.
                await asyncio.to_thread(
                    subprocess.run,
                    ["sudo", "-n", "true"],
                    check=False,
                    capture_output=True,
                )
        except asyncio.CancelledError:
            return


async def acquire_sudo(suspend: YieldTTY) -> bool:
    """Prompt for the sudo password via a macOS dialog and seed the timestamp.

    Uses `osascript` for the prompt because Textual's TTY suspend doesn't
    cleanly hand the terminal to interactive `sudo`. The `suspend` argument
    is kept for API compatibility but unused — the GUI dialog floats above
    the TUI on its own.

    Returns True if sudo was granted, False otherwise (cancelled or wrong
    password).
    """
    del suspend  # unused: GUI dialog doesn't need the TTY
    for _ in range(3):
        osa = await asyncio.create_subprocess_exec(
            "osascript", "-e", _OSASCRIPT_PROMPT,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, _ = await osa.communicate()
        if osa.returncode != 0:
            return False  # user clicked Cancel or hit Esc
        password = out.decode("utf-8", errors="replace").rstrip("\n")

        sudo = await asyncio.create_subprocess_exec(
            "sudo", "-S", "-v",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await sudo.communicate(input=(password + "\n").encode())
        if sudo.returncode == 0:
            return True
    return False
