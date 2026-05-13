"""Terminal.app custom profile import.

macOS Terminal.app reads .terminal profile files when opened with `open`.
This section opens the bundled profile so it's added to Terminal's Profile
list. The user then sets it as default manually in Terminal > Settings.

There's no scriptable way to set a profile as default — Apple holds that
preference in Terminal's plist with a UUID that's generated on import.
"""

from __future__ import annotations

import plistlib
import subprocess
from pathlib import Path

from macsetup.core.config import Item
from macsetup.core.paths import ASSETS_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


PROFILE_FILE = ASSETS_DIR / "custom.terminal"
TERMINAL_PLIST = Path.home() / "Library" / "Preferences" / "com.apple.Terminal.plist"


def _profile_name_from_file() -> str:
    """Read the profile's 'name' key from the .terminal plist."""
    try:
        with PROFILE_FILE.open("rb") as f:
            data = plistlib.load(f)
        return str(data.get("name", "custom"))
    except Exception:
        return "custom"


def _terminal_has_profile(name: str) -> bool:
    """Check whether Terminal.app's plist contains a profile with this name.

    Terminal stores profiles under "Window Settings" → name → dict.
    """
    if not TERMINAL_PLIST.exists():
        return False
    try:
        # Use `defaults read` rather than parsing plist directly — Terminal
        # uses CFKeyedArchiver inside its profile dicts, which plistlib
        # doesn't decode cleanly.
        result = subprocess.run(
            ["defaults", "read", "com.apple.Terminal", "Window Settings"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0 and name in result.stdout
    except (subprocess.SubprocessError, OSError):
        return False


class TerminalProfileSection(Section):
    name = "Terminal profile"
    description = "Custom Terminal.app profile (set as default manually after import)"

    async def detect(self) -> SectionStatus:
        if not PROFILE_FILE.exists():
            return SectionStatus(Status.PENDING, 0, 1, "Profile file missing in assets/")
        profile_name = _profile_name_from_file()
        if _terminal_has_profile(profile_name):
            return SectionStatus(Status.DONE, 1, 1)
        return SectionStatus(Status.PENDING, 0, 1)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not PROFILE_FILE.exists():
            await emit(f"Profile file missing at {PROFILE_FILE}")
            return
        profile_name = _profile_name_from_file()
        if _terminal_has_profile(profile_name):
            await emit(f"Terminal profile '{profile_name}' already imported")
            return
        await emit(f"open {PROFILE_FILE}")
        await run(["open", str(PROFILE_FILE)], on_line=emit)
        await emit(
            f"Profile '{profile_name}' imported into Terminal.app. "
            "Open Terminal > Settings > Profiles, select it, and click "
            "'Default' at the bottom to set it as default."
        )
