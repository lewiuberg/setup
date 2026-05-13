"""Mac App Store apps via mas-cli.

mas can install but cannot authenticate — Apple removed that API. The
section verifies the user is signed in to the App Store before
attempting installs, and surfaces a clear message otherwise.
"""

from __future__ import annotations

from macsetup.core.config import Item, load_items
from macsetup.core.detect import command_exists, installed_brews
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run, run_capture
from macsetup.sections.base import Emit, Section, SectionStatus, Status


async def _installed_app_ids() -> set[str]:
    if not command_exists("mas"):
        return set()
    result = await run_capture(["mas", "list"])
    if not result.ok:
        return set()
    # `mas list` output: "<id> <name> (version)"
    return {line.split(maxsplit=1)[0] for line in result.stdout.splitlines() if line.strip()}


async def _signed_in() -> bool:
    if not command_exists("mas"):
        return False
    result = await run_capture(["mas", "account"])
    # Older mas: prints an email and exits 0 when signed in.
    # Newer mas (deprecated `account`): returns non-zero. We treat ok as signed-in.
    return result.ok and "@" in result.stdout


class AppStoreSection(Section):
    name = "App Store"
    description = "Mac App Store apps via mas (sign in to App Store first)"
    config_file = "app_store.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        installed = await _installed_app_ids()
        count = sum(1 for item in items if str(item.extras.get("id", "")) in installed)
        total = len(items)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if count == total:
            return SectionStatus(Status.DONE, count, total)
        return SectionStatus(Status.PARTIAL, count, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if "mas" not in await installed_brews():
            await emit("Installing mas via brew…")
            result = await run(["brew", "install", "mas"], on_line=emit)
            if not result.ok:
                await emit(f"mas install failed: {result.stderr.strip()}")
                return

        if not await _signed_in():
            await emit(
                "Not signed in to the App Store. Open the App Store app, "
                "sign in with your Apple ID, then re-run this section."
            )
            return

        installed = await _installed_app_ids()
        for item in items:
            app_id = str(item.extras.get("id", ""))
            if not app_id:
                await emit(f"skipping {item.name}: missing `id` in TOML")
                continue
            if app_id in installed:
                await emit(f"already installed: {item.name}")
                continue
            await emit(f"mas install {app_id}  # {item.name}")
            result = await run(["mas", "install", app_id], on_line=emit)
            if not result.ok:
                await emit(f"failed: {item.name}: {result.stderr.strip()}")
