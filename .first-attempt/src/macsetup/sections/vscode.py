"""VS Code extensions via `code --install-extension <id>`."""

from __future__ import annotations

from macsetup.core.config import Item, load_items
from macsetup.core.detect import command_exists, installed_vscode_extensions
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


class VSCodeSection(Section):
    name = "VS Code"
    description = "VS Code extensions"
    config_file = "vscode_extensions.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        if not command_exists("code"):
            return SectionStatus(Status.PENDING, 0, len(items), "VS Code CLI missing")
        installed = await installed_vscode_extensions()
        count = sum(1 for item in items if item.name.lower() in installed)
        total = len(items)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if count == total:
            return SectionStatus(Status.DONE, count, total)
        return SectionStatus(Status.PARTIAL, count, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not command_exists("code"):
            await emit(
                "`code` CLI missing. Install via Casks (visual-studio-code), "
                "then in VS Code run 'Shell Command: Install code command in PATH'."
            )
            return
        installed = await installed_vscode_extensions()
        for item in items:
            if item.name.lower() in installed:
                await emit(f"already installed: {item.name}")
                continue
            await emit(f"code --install-extension {item.name}")
            result = await run(
                ["code", "--install-extension", item.name], on_line=emit
            )
            if not result.ok:
                await emit(f"failed: {item.name}: {result.stderr.strip()}")
