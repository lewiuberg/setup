"""macOS architecture detection and Homebrew path resolution.

Single source of truth. The old shell code checked `uname -m` in three
different places using two different idioms (`uname -m` vs `uname -p`);
this consolidates the decision.
"""

from __future__ import annotations

import platform
from enum import Enum
from pathlib import Path


class Arch(Enum):
    ARM64 = "arm64"
    X86_64 = "x86_64"


def detect() -> Arch:
    machine = platform.machine()
    if machine == "arm64":
        return Arch.ARM64
    if machine in ("x86_64", "i386"):
        return Arch.X86_64
    raise RuntimeError(f"Unsupported architecture: {machine!r}")


def brew_prefix(arch: Arch | None = None) -> Path:
    """Homebrew prefix for the architecture.

    Apple Silicon: /opt/homebrew
    Intel:         /usr/local
    """
    if arch is None:
        arch = detect()
    return Path("/opt/homebrew") if arch is Arch.ARM64 else Path("/usr/local")


def brew_bin(arch: Arch | None = None) -> Path:
    return brew_prefix(arch) / "bin" / "brew"
