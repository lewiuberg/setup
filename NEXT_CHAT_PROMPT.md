# Prompt for the next chat

Copy everything below the `---` line into the new chat as your first
message. `HANDOVER.md` at the repo root has the full context from the
first attempt — point me at it once we start.

---

I have moved the first attempt into `./.first-attempt/` and want to
start fresh. Please read [HANDOVER.md](HANDOVER.md) first for the
context from that attempt — what worked, what didn't land, and the
preferences I've already confirmed — so we don't relitigate decisions
that are already settled.

I also want you to analyse [`.old-root/automated-setup/`](.old-root/automated-setup/)
carefully — especially [install.sh](.old-root/automated-setup/install.sh),
[terminal.sh](.old-root/automated-setup/terminal.sh),
[configure_p10k.sh](.old-root/automated-setup/configure_p10k.sh) and
[notes.sh](.old-root/automated-setup/notes.sh). That code worked well
end-to-end before the Poetry 2.x bug broke it; the new wizard should
follow its structure closely rather than reinvent things.

**Caveat:** much of that legacy code was written 3–5 years ago, so some
of its choices may be outdated — pinned formula URLs, deprecated taps
(`homebrew/cask-fonts`), commands that have since changed flags or been
removed (the Poetry 2.x failure is one example), plugins that have
better modern equivalents. As you go through each step, flag anything
that looks stale and propose a current alternative before we wire it in.

## What I want this time

A setup **wizard** (CLI/TUI) that does much of what
[`.old-root/automated-setup/install.sh`](.old-root/automated-setup/install.sh)
does, but with finer control than the old plain shell scripts gave me.

If you spot improvements to any of the steps below — order, scope,
breaking a step into smaller ones, anything — flag them and propose
alternatives before we commit. I'd rather hear "this could be better
done as X" than have you silently follow my list.

## Step-by-step flow

(Maybe the the steps should be combined og divided better, but this is how the old script worked from my understanding, so let's start here and iterate.)

1. Create `~/.zprofile` and `~/.zshrc` if missing (Or shold these be generated later in the "pipeline"?), then ask me whether I
   want Rosetta 2.
2. Check whether Homebrew is installed; if not, ask whether to install
   it. Run `brew doctor` and `brew update`.
3. Show a list of taps. Let me skip the section entirely, or untick
   individual entries.
4. Show a list of brew packages. Same — skip-all or per-item.
5. Show a list of casks. Same — skip-all or per-item.
6. Run `brew cleanup`.
7. Install Oh My Zsh. For this and every subsequent install, check
   whether it's already installed first.
8. Append the `ZSHRC_ARCHITETURE` block from
   [terminal.sh](.old-root/automated-setup/terminal.sh) to `~/.zshrc`.
9. Install Powerlevel10k. If `~/.p10k.zsh` isn't configured yet, let me
   run the p10k configurator interactively before moving on.
10. Apply the custom p10k modifications from
    [configure_p10k.sh](.old-root/automated-setup/configure_p10k.sh).
11. Install zsh-syntax-highlighting, zsh-autosuggestions,
    zsh-autoswitch-virtualenv, and pyenv. Append the matching blocks to
    `~/.zshrc`. Create `~/.warprc` with the shortcuts from the legacy
    script.
12. Install Poetry (for legacy projects) and uv (for new projects).
    Apply the version-aware Poetry fix from the handover doc.
13. Install asdf and plugins for the runtimes I'll use (dotnet, go,
    node, rust, …).
14. Append the aliases block from terminal.sh to `~/.zshrc`.
15. Install Raycast. If there's a programmatic install path for a list
    of extensions, use it. Otherwise, open the Raycast Store URL for
    each extension in the browser one by one so I can install manually.
16. Same pattern for the apps in
    [manual_installations.sh](.old-root/automated-setup/manual_installations.sh)
    — preferably automated via `mas`, otherwise opened one by one.

## Generated usage guide

When the wizard finishes, generate an HTML usage reference at
`~/MACSETUP-USAGE.html` containing:
- The notes from [notes.sh](.old-root/automated-setup/notes.sh) (pyenv
  usage, Poetry usage, zsh-autoswitch usage)
- Any other reference material that fits — relevant aliases, the
  `~/.warprc` shortcuts, the Raycast extensions I picked, etc.

Style it like the `example.html` from another project of mine (I'll
share that file in the chat). Open the file automatically when the
wizard completes.

## Dotfiles

**Do not symlink the dotfiles** — generate them from the wizard
directly into `$HOME`. (The first attempt symlinked from a `dotfiles/`
folder in the repo; I prefer generated files for this project.)

## Reset / undo (lower priority — only after the main wizard works)

If feasible, add an option to reset what the wizard has done — undo the
installs and revert the dotfile changes — so I can run it again from a
clean slate while we iterate on the UX. This is not a blocker; ship
the wizard first, add reset after.

## Interview me

Before you start coding, interview me for any clarifications you need —
order, scope, exact wording in the HTML guide, anything ambiguous. The
handover doc lists some open questions worth asking.
