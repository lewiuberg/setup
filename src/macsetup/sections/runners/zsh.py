"""Runners for the Zsh family: Oh My Zsh, Powerlevel10k (install only), and the
non-autoswitch zsh plugins (syntax-highlighting, autosuggestions).

Configuration of the dotfiles (~/.zshrc, ~/.p10k.zsh) lives in the dotfiles
section — these runners only get the binaries / plugins onto disk.
"""
from __future__ import annotations

import os
from pathlib import Path

from macsetup.core.executor import Executor
from macsetup.sections.base import Section
from macsetup.sections.runners import register_runner

OMZ_DIR = Path.home() / ".oh-my-zsh"
ZSH_CUSTOM = OMZ_DIR / "custom"

OMZ_INSTALLER = (
    'sh -c "$(curl -fsSL '
    'https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
)

PLUGINS = {
    "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git",
    "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions.git",
}

P10K_REPO = "https://github.com/romkatv/powerlevel10k.git"
P10K_DIR = ZSH_CUSTOM / "themes" / "powerlevel10k"


@register_runner("oh_my_zsh")
async def run_oh_my_zsh(section: Section, items: set[str], executor: Executor) -> bool:
    if OMZ_DIR.exists():
        executor.log(f"  [#4ec9b0]✓[/] Oh My Zsh already at {OMZ_DIR}")
        return True
    executor.log("  installing Oh My Zsh (unattended)…")
    env = {**os.environ, "RUNZSH": "no", "CHSH": "no", "KEEP_ZSHRC": "yes"}
    proc = await executor.shell.run(["sh", "-c", OMZ_INSTALLER], env=env)
    if proc.exit_code != 0:
        executor.log(f"  [#f44747]Oh My Zsh installer exited {proc.exit_code}[/]")
        for line in proc.output.splitlines()[-10:]:
            executor.log(f"    {line}")
        return False
    executor.log(f"  [#4ec9b0]✓[/] installed at {OMZ_DIR}")
    return True


@register_runner("powerlevel10k")
async def run_powerlevel10k(section: Section, items: set[str], executor: Executor) -> bool:
    if not OMZ_DIR.exists():
        executor.log("  [#f44747]Oh My Zsh required first[/]")
        return False
    if P10K_DIR.exists():
        executor.log(f"  [#4ec9b0]✓[/] Powerlevel10k already at {P10K_DIR}")
    else:
        executor.log(f"  cloning Powerlevel10k → {P10K_DIR}…")
        code = await executor.shell.stream(
            ["git", "clone", "--depth=1", P10K_REPO, str(P10K_DIR)],
            lambda line: executor.log(f"    {line}"),
        )
        if code != 0:
            executor.log(f"  [#f44747]git clone exited {code}[/]")
            return False

    if (Path.home() / ".p10k.zsh").exists():
        executor.log(f"  [#4ec9b0]✓[/] ~/.p10k.zsh already present, skipping configurator")
        return True

    if executor.dry_run:
        executor.log("  [#ce9178][dry-run][/] would pause for `p10k configure` in a new terminal")
        return True

    # Yield the TTY and prompt the user. They open a NEW terminal — the freshly
    # written ~/.zshrc (rendered in the dotfiles section earlier) sources p10k,
    # which auto-runs `p10k configure` because ~/.p10k.zsh is missing.
    executor.log("  [#ce9178]pausing for Powerlevel10k configuration…[/]")
    with executor.suspend():
        print()
        print("─" * 64)
        print("Powerlevel10k is installed but not configured yet.")
        print()
        print("To configure it now (recommended):")
        print("  1. Open a NEW terminal window or tab")
        print("  2. The p10k configurator will start automatically")
        print("  3. Complete the wizard — it writes ~/.p10k.zsh")
        print("  4. Come back here and press Enter")
        print()
        print("Or just press Enter to skip; you can run `p10k configure`")
        print("from a new terminal whenever you like.")
        print("─" * 64)
        try:
            input("\nPress Enter to continue the macsetup wizard… ")
        except EOFError:
            pass

    if (Path.home() / ".p10k.zsh").exists():
        executor.log("  [#4ec9b0]✓[/] ~/.p10k.zsh written — p10k is configured")
    else:
        executor.log(
            "  [#ce9178]~/.p10k.zsh not yet present; run `p10k configure` "
            "from a new terminal later.[/]"
        )
    return True


@register_runner("zsh_plugins")
async def run_zsh_plugins(section: Section, items: set[str], executor: Executor) -> bool:
    if not OMZ_DIR.exists():
        executor.log("  [#f44747]Oh My Zsh required first[/]")
        return False
    plugins_dir = ZSH_CUSTOM / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    for name, url in PLUGINS.items():
        target = plugins_dir / name
        if target.exists():
            executor.log(f"  [#4ec9b0]✓[/] {name} (already present)")
            continue
        executor.log(f"  cloning {name}…")
        code = await executor.shell.stream(
            ["git", "clone", "--depth=1", url, str(target)],
            lambda line: executor.log(f"    {line}"),
        )
        if code != 0:
            executor.log(f"  [#f44747]{name} clone exited {code}[/]")
    return True
