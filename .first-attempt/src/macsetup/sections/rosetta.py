"""Rosetta 2 — Apple Silicon compatibility layer for x86 binaries.

Single-step section: either installed or not. Requires sudo.
"""

from __future__ import annotations

from pathlib import Path

from macsetup.core.arch import Arch
from macsetup.core.arch import detect as detect_arch
from macsetup.core.config import Item
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


ROSETTA_MARKER = Path("/Library/Apple/usr/share/rosetta/rosetta")


class RosettaSection(Section):
    name = "Rosetta"
    description = "Apple Silicon compatibility for x86 binaries"
    requires_sudo = True

    async def detect(self) -> SectionStatus:
        if detect_arch() is Arch.X86_64:
            return SectionStatus(Status.DONE, 1, 1, "Not required on Intel")
        if ROSETTA_MARKER.exists():
            return SectionStatus(Status.DONE, 1, 1)
        return SectionStatus(Status.PENDING, 0, 1)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if detect_arch() is Arch.X86_64:
            await emit("Skipping — not on Apple Silicon")
            return
        if ROSETTA_MARKER.exists():
            await emit("Rosetta is already installed")
            return
        await emit("Installing Rosetta 2 (requires sudo)…")
        result = await run(
            ["sudo", "softwareupdate", "--install-rosetta", "--agree-to-license"],
            on_line=emit,
        )
        if result.ok:
            await emit("Rosetta 2 installed")
        else:
            await emit(f"Rosetta 2 install failed: {result.stderr.strip()}")
