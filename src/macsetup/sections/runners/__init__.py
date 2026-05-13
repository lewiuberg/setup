"""Section runner registry and protocol.

A runner is `async (Section, set[str], Executor) -> bool`. Each per-section
module registers its runner via `@register_runner("<slug>")` at import time.
Importing this package imports all built-in runner modules so the registry
fills automatically.
"""
from __future__ import annotations

from typing import Awaitable, Callable

from macsetup.core.executor import Executor
from macsetup.sections.base import Section

Runner = Callable[[Section, set[str], Executor], Awaitable[bool]]

RUNNERS: dict[str, Runner] = {}


def register_runner(slug: str) -> Callable[[Runner], Runner]:
    def decorator(fn: Runner) -> Runner:
        RUNNERS[slug] = fn
        return fn

    return decorator


def get_runner(slug: str) -> Runner | None:
    return RUNNERS.get(slug)


# Side-effect imports register runners.
from macsetup.sections.runners import apps  # noqa: E402, F401
from macsetup.sections.runners import auth  # noqa: E402, F401
from macsetup.sections.runners import brew  # noqa: E402, F401
from macsetup.sections.runners import devtools  # noqa: E402, F401
from macsetup.sections.runners import dotfiles  # noqa: E402, F401
from macsetup.sections.runners import html_guide  # noqa: E402, F401
from macsetup.sections.runners import python_tools  # noqa: E402, F401
from macsetup.sections.runners import vscode  # noqa: E402, F401
from macsetup.sections.runners import zsh  # noqa: E402, F401
