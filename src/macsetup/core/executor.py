from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Awaitable, Callable

from macsetup.core.shell import Shell
from macsetup.core.sudo import SudoKeepalive
from macsetup.state import PlanState

LogFn = Callable[[str], None]
SuspendFn = Callable[[], AbstractContextManager[None]]
EnsureSudoFn = Callable[[], Awaitable[bool]]


@dataclass
class Executor:
    """Context passed to each section runner.

    Runners get a `shell` for subprocess work, `log`/`progress` for TUI
    output, `suspend` for yielding the terminal (interactive subprocesses),
    `ensure_sudo` to lazily acquire sudo, and the user's `state` for any
    cross-section coordination.

    `dry_run` is True when the user passed `--dry-run`. Runners that bypass
    `shell` (direct `subprocess.run`, file writes, browser opens) MUST check
    this flag and short-circuit to logging.
    """

    shell: Shell
    log: LogFn
    progress: LogFn
    suspend: SuspendFn
    ensure_sudo: EnsureSudoFn
    state: PlanState
    keepalive: SudoKeepalive
    dry_run: bool = False
