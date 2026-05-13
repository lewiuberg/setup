"""External zsh plugins — git-cloned into ~/.oh-my-zsh/custom/plugins/.

Built-in OMZ plugins (brew, git, gh, wd, etc.) don't need installation —
they're enabled via the `plugins=(…)` array in dotfiles/.zshrc and load
automatically. This section only handles plugins of type = "git".
"""

from __future__ import annotations

from pathlib import Path

from macsetup.core.config import Item, load_items
from macsetup.core.paths import CONFIG_DIR
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


OMZ_CUSTOM_PLUGINS = Path.home() / ".oh-my-zsh" / "custom" / "plugins"


def _external_plugins(items: list[Item]) -> list[Item]:
    return [i for i in items if i.extras.get("type") == "git"]


class ZshPluginsSection(Section):
    name = "zsh plugins"
    description = "External zsh plugins (git-cloned)"
    config_file = "zsh_plugins.toml"

    async def detect(self) -> SectionStatus:
        items = load_items(CONFIG_DIR / self.config_file)  # type: ignore[arg-type]
        external = _external_plugins(items)
        installed = sum(1 for p in external if (OMZ_CUSTOM_PLUGINS / p.name).exists())
        total = len(external)
        if total == 0:
            return SectionStatus(Status.DONE, 0, 0, "No external plugins configured")
        if installed == 0:
            return SectionStatus(Status.PENDING, 0, total)
        if installed == total:
            return SectionStatus(Status.DONE, installed, total)
        return SectionStatus(Status.PARTIAL, installed, total)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if not OMZ_CUSTOM_PLUGINS.parent.exists():
            await emit(
                "Oh My Zsh not installed yet — run the Oh My Zsh section first"
            )
            return
        OMZ_CUSTOM_PLUGINS.mkdir(parents=True, exist_ok=True)
        for plugin in _external_plugins(items):
            target = OMZ_CUSTOM_PLUGINS / plugin.name
            if target.exists():
                await emit(f"already cloned: {plugin.name}")
                continue
            repo = plugin.extras.get("repo")
            if not repo:
                await emit(f"skipping {plugin.name}: no `repo` set in TOML")
                continue
            await emit(f"git clone {repo} → {target}")
            result = await run(["git", "clone", repo, str(target)], on_line=emit)
            if not result.ok:
                await emit(f"failed: {plugin.name}: {result.stderr.strip()}")
