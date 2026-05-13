# Plan — Modernise the macOS Setup Tool

## Context

The current setup tool (`./.old-root/automated-setup/`) is ~1,400 lines of zsh that runs linearly with no navigation, no resume, no section-level rerun, brittle `sed`-based dotfile editing (336-line `functions.sh` mega-utility), a monolithic 487-line `terminal.sh`, and several places where sudo can re-prompt during a run. The last attempted run failed at the Poetry step because Poetry 2.x removed the `virtualenvs.prefer-active-python` config key — `set -e` then aborted the entire run.

The intent is a full rewrite: a Python + Textual TUI driven by TOML config, with section-level navigation (jump-to / step-back), per-item checklists, one-time sudo entry kept alive in the background, symlinked dotfiles managed from the repo, live system detection (no state file), uv-managed Python deps, and App Store installs via `mas`. `.old-root/` stays untouched as a read-only reference.

---

## New file & folder structure

Everything new lives at the repo root alongside (not inside) `.old-root/`.

```text
/Users/lewiuberg/Repositories/setup/
├── .old-root/                       # READ-ONLY archive — never touched
├── .vscode/                         # existing
├── .gitignore                       # new (carried over from .old-root, trimmed)
├── .python-version                  # uv-managed pin
├── README.md                        # new, concise — purpose + how to run
├── PLAN.md                          # this plan
├── bootstrap.sh                     # entrypoint: install uv if missing, sync deps, launch TUI
├── pyproject.toml                   # uv project (textual, tomlkit, rich, click)
├── uv.lock
│
├── config/                          # declarative install lists (TOML)
│   ├── taps.toml
│   ├── brews.toml                   # name, description, required, category
│   ├── casks.toml
│   ├── fonts.toml
│   ├── app_store.toml               # mas IDs + names
│   ├── vscode_extensions.toml
│   ├── raycast_extensions.toml      # Store URLs (free tier — no CLI install)
│   ├── zsh_plugins.toml
│   ├── python_tools.toml            # pyenv versions, uv, poetry, etc.
│   ├── secrets.toml                 # expected key paths (no key material)
│   └── defaults.toml                # default ticked/unticked per section
│
├── dotfiles/                        # canonical dotfiles, symlinked to $HOME
│   ├── .zshrc
│   ├── .zprofile
│   ├── .p10k.zsh
│   ├── .tmux.conf
│   └── .gitconfig.template          # rendered with user values
│
├── assets/                          # binary/non-text resources copied (not symlinked)
│   ├── custom.terminal
│   └── Open-in-VSCode.workflow/
│
├── src/macsetup/                    # Python package
│   ├── __init__.py
│   ├── __main__.py                  # `python -m macsetup`
│   ├── app.py                       # Textual App, screen routing, keymap
│   │
│   ├── screens/                     # TUI screens
│   │   ├── home.py                  # section list with live status
│   │   ├── section.py               # per-section checklist + run
│   │   ├── progress.py              # live log during run
│   │   ├── sudo_modal.py            # one-time password prompt
│   │   └── help.py
│   │
│   ├── sections/                    # one module per install concern, all implement Section ABC
│   │   ├── base.py                  # Section, Item, Status, run/check protocol
│   │   ├── rosetta.py
│   │   ├── homebrew.py              # install brew + arch-aware path
│   │   ├── taps.py
│   │   ├── brews.py
│   │   ├── casks.py
│   │   ├── fonts.py
│   │   ├── app_store.py             # mas + Apple ID check
│   │   ├── oh_my_zsh.py
│   │   ├── powerlevel10k.py
│   │   ├── pyenv.py
│   │   ├── python_tools.py          # poetry, uv — version-aware config
│   │   ├── direnv.py
│   │   ├── dotnet.py
│   │   ├── zsh_plugins.py
│   │   ├── dotfiles.py              # symlink manager (with backup)
│   │   ├── vscode.py                # extensions
│   │   ├── raycast.py               # cask + extension Store URL flow
│   │   ├── secrets.py               # SSH/GPG key restore from user-supplied backup
│   │   └── terminal_profile.py     # Terminal.app .terminal import
│   │
│   ├── core/
│   │   ├── sudo.py                  # prompt-once + asyncio keep-alive task
│   │   ├── shell.py                 # async subprocess wrapper, captures stdout/stderr to log pane
│   │   ├── arch.py                  # arm64 vs x86_64; single source of truth
│   │   ├── detect.py                # is_installed(brew|cask|extension|file|line-in-file)
│   │   ├── config.py                # TOML loader, schema validation
│   │   ├── symlink.py               # safe symlink with timestamped backup of existing files
│   │   └── logging.py               # structured run log under ~/.local/state/macsetup/
│   │
│   └── ui/
│       ├── dark_plus.tcss           # Textual CSS theme — VS Code Default Dark+ palette
│       └── widgets.py               # framed header, status bar, checklist row
│
└── tests/
    ├── test_config.py               # TOML schema sanity
    ├── test_detect.py
    └── test_symlink.py
```

### Why this layout

- `config/` and `dotfiles/` are flat and editable without reading code — anything the user might tweak lives outside `src/`.
- `sections/` is the only place install logic lives. Each section is self-contained: TOML key → check function → install function → render rows. Adding a new section is one file.
- `core/` separates cross-cutting concerns (sudo, shell, arch, detection) so they can't be re-implemented inconsistently the way they are in the current scripts.
- `assets/` keeps binary/macOS-specific blobs out of `dotfiles/` (which is purely symlinkable text).
- `bootstrap.sh` is the only shell code — kept minimal (under ~40 lines): detect/install uv, `uv sync`, `uv run python -m macsetup`.

---

## UI / navigation design

**Visual style (chosen):**

- **Layout:** single-column list on Home — vertical, scannable, one section per row.
- **Status indicator:** small progress bar per row showing fraction complete (full bar = done, partial fill = X of N installed, empty = pending, hatched = error). For single-step sections (e.g. Rosetta) the bar is either full or empty.
- **Icons:** Nerd Font glyphs (Apple, beer mug, snake, etc.) prefixed to each section name. MesloLG Nerd Font is installed by the Fonts section, so any iTerm/Terminal profile that uses it will render them. Falls back to a generic box if the font is missing.
- **Theme:** custom Textual theme matching VS Code "Default Dark+": background `#1e1e1e`, foreground `#d4d4d4`, accent blue `#007acc`, selection `#264f78`, success green `#6a9955`, error red `#f44747`, warning yellow `#dcdcaa`, comment grey `#6a9955`. Encoded in `src/macsetup/ui/dark_plus.tcss`.

**Chrome (taking visual cues from [Posting](https://github.com/darrenburns/posting)):**

- Thin **header bar** at top with app name + version, persistent across screens.
- **Footer** (Textual's `Footer` widget) showing live key bindings inline, e.g. `^q quit  ^? help  esc back  r refresh  / filter`. Updates when entering a new screen.
- **Tabs** inside Section view: `Items` (the checklist), `Log` (last-run output for this section), `Notes` (section-specific help text from TOML). `Tab` / `Shift+Tab` to cycle.
- Progress view uses `RichLog(highlight=True, markup=True)` so subprocess output gets syntax-highlighted (URLs, paths, error keywords) and TUI-emitted notes can use Rich markup for emphasis.
- Same VS Code Default Dark+ palette throughout; tabs and footer use the accent blue `#007acc` for active state.

**Three screens, all keyboard-driven:**

1. **Home** — single-column list of sections (Rosetta, Homebrew, Brews, Casks, Fonts, App Store, Oh My Zsh, p10k, pyenv, Python tools, direnv, .NET, zsh plugins, Dotfiles, VS Code, Terminal profile). Each row: ` icon  Section name        ██████░░  14 / 16`. Detection runs at screen entry via `core/detect.py`. Arrow keys move, Enter opens.

2. **Section** — per-item checklist (DataTable with checkbox column). Items pre-ticked per `config/defaults.toml` and skipped if already installed. Space toggles, `a` ticks all, `n` unticks all, Enter runs only the ticked items, `Esc` returns home without running.

3. **Progress** — live log streaming subprocess output (Textual `RichLog`) with a header bar showing the same progress bar style, ticking forward as items complete. `Esc` aborts current step and returns to section view; finished items get a filled bar on the checklist behind it.

**Global keymap:** `Esc` = back, `q` = quit, `?` = help, `r` = re-detect status on Home, `/` = filter sections.

**Sudo:** on first launch (or first time a section actually needs root), a modal prompts once. Password is fed to `sudo -v` via stdin then discarded. An asyncio task runs `sudo -n -v` every 60s for the rest of the session so no later step re-prompts. Modal redisplays only if the cached credential expires (e.g. machine sleep > sudo timeout).

---

## Configuration model (TOML)

Single shape across all section TOMLs:

```toml
# config/brews.toml
[[item]]
name = "git"
description = "Distributed version control"
required = true
category = "core"

[[item]]
name = "tmux"
description = "Terminal multiplexer"
required = false
category = "terminal"
```

`config/defaults.toml` says whether a category is ticked by default. Comments in the TOML carry the rationale that today lives as `# commented out` lines in `brew_formulas.sh`.

`config/python_tools.toml` carries version-aware notes so the Poetry/uv section knows e.g. `prefer-active-python` only applies to Poetry < 2.0.

---

## Fix for the install.sh error

Root cause: `poetry config virtualenvs.prefer-active-python true` is invalid on Poetry ≥ 2.0; `set -e` then kills the entire run.

New behaviour, in `sections/python_tools.py`:

1. Detect installed Poetry version with `poetry --version`.
2. If Poetry < 2.0: set `virtualenvs.prefer-active-python true`.
3. If Poetry ≥ 2.0: skip (default is already to use the active Python; the equivalent control is `virtualenvs.use-poetry-python` which defaults to `false`).
4. Step-level errors are caught, logged, and surfaced as a `✗` on that one row — they never abort sibling steps or the run as a whole. Only a Section can decide it's fatal (e.g. Homebrew install failure aborts dependent sections).

Any `pyproject.toml` the tool writes uses `[tool.poetry.group.dev.dependencies]` (not the deprecated `poetry.dev-dependencies`).

---

## Dotfile strategy (symlink with backup)

`sections/dotfiles.py` does, for each file in `dotfiles/`:

1. Target = `$HOME/<filename>`.
2. If target is already a symlink pointing at the repo file → skip.
3. If target exists and differs → move to `$HOME/.macsetup-backups/<timestamp>/<filename>` and report path in the log.
4. Create symlink `$HOME/<filename>` → `<repo>/dotfiles/<filename>`.

`.gitconfig` is rendered from `.gitconfig.template` using values collected in a one-time first-run dialog (name, email) stored in `config/user.toml` (gitignored).

---

## Bootstrap

`bootstrap.sh` (≈30 lines):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 1. Ensure uv is available (preinstalled via brew, otherwise curl install)
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sync deps into managed venv, using macOS system Python (/usr/bin/python3).
#    Do NOT install a separate Python for the tool itself — pyenv is the only
#    Python installer this project recognises, and pyenv may not exist yet on
#    a fresh machine. System Python is preinstalled on every supported macOS.
uv sync --quiet --python /usr/bin/python3

# 3. Launch the TUI
exec uv run python -m macsetup "$@"
```

`pyproject.toml` pins `requires-python = ">=3.9"` to match macOS system Python's floor. The tool's venv is the only Python it touches; pyenv-installed Pythons are for the user's own projects.

No global Python pollution. Re-running the same script is the supported way to re-enter the tool.

## Python tools: uv first, Poetry as legacy

uv for all new projects; Poetry only for legacy projects. `sections/python_tools.py` reflects this:

- `uv` is a required item, defaulted on.
- `poetry` is an optional item, defaulted off. Present so legacy projects can be opened on the new machine without a separate install dance.
- When Poetry *is* ticked, the version-aware fix kicks in (see *Fix for the install.sh error*).

`config/python_tools.toml`:

```toml
[[item]]
name = "uv"
description = "Fast Python project & package manager (primary for new projects)"
required = true
default = true

[[item]]
name = "poetry"
description = "Python dependency manager (legacy projects only)"
required = false
default = false
```

## Python version management (pyenv section)

`sections/pyenv.py` handles installing `pyenv` + `pyenv-virtualenv` via brew (already covered) and writing the `pyenv init` lines into `dotfiles/.zshrc` / `.zprofile`. It then offers — per checklist item — installing each Python version listed in `config/python_tools.toml`:

```toml
[pyenv]
versions = ["3.11.9", "3.12.5", "3.13.0"]
# global = "..."   # NOT supported by design
```

**Explicitly never sets a global pyenv version.** No `pyenv global X` is ever invoked. The TUI shows a note on the section screen explaining how to use `pyenv local <version>` inside a project directory (writes `.python-version`) or `pyenv shell <version>` for a single shell. The setup tool's own venv is unaffected because it lives on system Python, not on pyenv shims.

A sanity check on every run: if `~/.pyenv/version` exists (the marker `pyenv global` writes), the section flags it as `⊙ partial` and offers to remove it. Never auto-removes.

---

## SSH / GPG key import (secrets section)

A fresh Mac with no SSH or GPG keys can't push to GitHub, sign commits, or reach servers. `sections/secrets.py` handles restoration from a user-supplied backup — it never contains, generates, or transmits key material itself.

**Repo never holds keys.** `config/secrets.toml` only declares *which files are expected to exist* and where they belong, with sensible defaults:

```toml
[[item]]
name = "ssh-private"
path = "~/.ssh/id_ed25519"
mode = "0600"
add_to_keychain = true

[[item]]
name = "ssh-public"
path = "~/.ssh/id_ed25519.pub"
mode = "0644"

[[item]]
name = "ssh-config"
path = "~/.ssh/config"
template = "dotfiles/.ssh/config.template"   # rendered from repo, safe to commit

[[item]]
name = "gpg-pubring"
path = "~/.gnupg/pubring.kbx"
mode = "0600"

[git-signing]
enable = true                                 # sets commit.gpgsign true, gpg.program gpg
```

**Flow per checklist item:**

1. Detect: does the file exist at `path`? If yes → tick as done.
2. If missing, the section prompts (one modal, all items at once): *"Source for SSH/GPG keys?"* with options: `path to tar.gz/zip`, `mounted volume`, `1Password CLI (op item get …)`, `skip — restore manually`.
3. Copy / decrypt into place; `chmod` to the declared `mode`; `chmod 700 ~/.ssh` and `~/.gnupg`.
4. If `add_to_keychain = true`: run `ssh-add --apple-use-keychain <path>` (macOS keychain integration so passphrase is asked once).
5. For `[git-signing]`: `git config --global commit.gpgsign true`, `git config --global gpg.program $(which gpg)`, and prompt for the signing key ID (read from `gpg --list-secret-keys` after import).

**Out of scope:** generating new keys (`ssh-keygen`, `gpg --gen-key`) and adding them to GitHub. Account-specific and a manual step the user owns.

The section appears in the Home list with the same status-bar treatment as the others: empty bar if nothing detected, full when all expected files are present and permissions are correct.

## Raycast (free tier — no programmatic install for extensions)

Verified against Raycast's own docs: deep-links like `raycast://extensions/<author>/<extension>/<command>` only *run* commands that are already installed. There is no documented deep-link to install an extension from the Store, and no Raycast CLI. Cloud Sync would solve this in one shot, but it's a Pro-only feature and you're on the free tier.

The Raycast section therefore takes a **browser-hand-off** approach, similar to the App Store fallback:

`config/raycast_extensions.toml`:

```toml
# Raycast Store URLs. The TUI opens each ticked URL in your browser;
# clicking "Install Extension" on the Store page hands off to Raycast,
# where one Return press completes the install. Detection looks for
# matching folders under ~/Library/Application Support/com.raycast.macos/extensions/.

[[item]]
name = "thomas/visual-studio-code"
description = "Search VS Code recent projects"
url = "https://www.raycast.com/thomas/visual-studio-code"
default = true

[[item]]
name = "raycast/github"
description = "GitHub repos, PRs, issues, actions"
url = "https://www.raycast.com/raycast/github"
default = true
```

`sections/raycast.py` flow:

1. Check `/Applications/Raycast.app` — if missing, install via `brew install --cask raycast`.
2. `open -a Raycast` so the menubar process is running (required for the `raycast://` hand-off to work from the browser).
3. Detect installed extensions by listing folders in `~/Library/Application Support/com.raycast.macos/extensions/` and matching their slugs against the TOML. Already-installed items pre-tick as done.
4. For each ticked-but-not-installed item: `open <url>`, with a short delay between opens so tabs don't race. The TUI shows a note: *"For each tab that opens, click Install Extension → Raycast will take focus → press Return."*
5. Note about Pro: if the user later upgrades to Pro, signing in to Cloud Sync supersedes this section entirely.

This is the best-available reliability without Pro. If Raycast publishes a Store-install deep-link in future, the section is one-line away from full automation — just swap the `open <https-url>` for `open <raycast-url>`.

## Extensibility — how to add/remove things

**Add or remove a single program (brew, cask, font, App Store app, VS Code extension, zsh plugin, Python tool):**
Edit the matching TOML file under `config/`. Each entry is an `[[item]]` block. The TUI picks up the change on next launch — no code edit, no rebuild.

```toml
# config/casks.toml — add Arc browser
[[item]]
name = "arc"
description = "The browser from The Browser Company"
required = false
category = "browser"
default = true
```

Removing = delete or comment out the block.

**Add a whole new section** (say, Docker config or Nix install) — three steps:

1. Create `src/macsetup/sections/docker.py` implementing the `Section` ABC from `sections/base.py`:

   ```python
   class DockerSection(Section):
       name = "Docker"
       icon = ""       # Nerd Font docker glyph
       config_file = "config/docker.toml"   # optional

       def detect(self) -> SectionStatus: ...
       async def install(self, items: list[Item], log) -> None: ...
   ```

2. Register it in `src/macsetup/sections/__init__.py` — one line appended to the ordered `SECTIONS` list. Order = display order on Home.

3. (Optional) Add `config/docker.toml` for the per-item checklist.

The ABC enforces: each section is responsible for its own detection, its own install steps, and reporting status back to the TUI. Sections cannot reach into each other's state — cross-cutting concerns must use `core/` (sudo, shell, arch, detect, symlink). A broken or experimental section can't take down the rest of the tool.

**Reordering sections:** rearrange the `SECTIONS` list in `sections/__init__.py`. No other changes.

**Disabling a section without deleting it:** comment the line out in `sections/__init__.py`, or set `enabled = false` in the section's TOML (the loader skips it).

## What gets salvaged from `.old-root/` (by reading only)

- Package lists from `brew_formulas.sh` → split into `config/{taps,brews,casks,fonts}.toml`.
- VS Code extension list from `vscode_extensions.sh` → `config/vscode_extensions.toml`.
- Manual App Store list from `manual_installations.sh` → `config/app_store.toml` with mas IDs added.
- `.p10k.zsh`, `.tmux.conf` → copied verbatim into `dotfiles/`.
- `custom.terminal`, `Open in VSCode.workflow/` → copied into `assets/`.
- The p10k tweak logic from `configure_p10k.sh` → re-expressed as the desired final `.p10k.zsh` content directly (no more in-place sed editing).
- The `.zshrc` / `.zprofile` content that the old scripts *append* → assembled once into the canonical `dotfiles/.zshrc` and `dotfiles/.zprofile`.

Nothing in `.old-root/` is moved, modified, or deleted.

---

## README illustrations

The README ships with visuals — not optional decoration, they're the easiest way to grok the tool.

**Real TUI screenshots** generated by Textual's built-in SVG snapshot:

- `assets/screenshots/home.svg` — Home screen with mixed-status sections.
- `assets/screenshots/section.svg` — Section view with per-item checklist.
- `assets/screenshots/progress.svg` — Progress view with live log + progress bar.
- `assets/screenshots/sudo.svg` — One-time sudo modal.

These are captured by a small `scripts/capture_screenshots.py` that drives the app with `Pilot` (Textual's test harness), feeds canned state, and calls `App.save_screenshot(path)`. Re-runnable on every UI change so screenshots never go stale.

**Mermaid diagrams** rendered inline by GitHub:

- Bootstrap flow: `bootstrap.sh` → uv install → uv sync (system Python) → `python -m macsetup` → TUI.
- Dotfile symlink flow: existing file? → backup to `~/.macsetup-backups/<timestamp>/` → symlink `~/<file>` → `<repo>/dotfiles/<file>`.
- Section lifecycle: detect → render checklist → user ticks → run items (async) → re-detect → return status.

Embedded directly in `README.md` with relative links so they render on GitHub without external hosting.

---

## Critical files to create

- [bootstrap.sh](bootstrap.sh) — entry script
- [pyproject.toml](pyproject.toml) — uv project, deps: `textual`, `tomlkit`, `rich`, `click`
- [src/macsetup/app.py](src/macsetup/app.py) — Textual app + routing
- [src/macsetup/sections/base.py](src/macsetup/sections/base.py) — `Section` / `Item` ABC, run protocol
- [src/macsetup/core/sudo.py](src/macsetup/core/sudo.py) — one-shot prompt + keep-alive
- [src/macsetup/core/shell.py](src/macsetup/core/shell.py) — async subprocess with live log
- [src/macsetup/core/arch.py](src/macsetup/core/arch.py) — single arch/brew-path source of truth
- [src/macsetup/core/detect.py](src/macsetup/core/detect.py) — `brew_installed`, `cask_installed`, `vscode_extension_installed`, `line_in_file`, `is_symlink_to`
- [src/macsetup/core/symlink.py](src/macsetup/core/symlink.py) — symlink with timestamped backup
- [src/macsetup/sections/python_tools.py](src/macsetup/sections/python_tools.py) — version-aware Poetry config (fixes the reported error)
- [config/](config/) — all TOML lists
- [dotfiles/](dotfiles/) — canonical dotfiles
- [src/macsetup/ui/dark_plus.tcss](src/macsetup/ui/dark_plus.tcss) — VS Code Default Dark+ theme
- [scripts/capture_screenshots.py](scripts/capture_screenshots.py) — Textual Pilot screenshotter
- [README.md](README.md) — purpose, illustrated walkthrough, `./bootstrap.sh` instruction

---

## Implementation phases

1. **Scaffold** — create folder skeleton, `pyproject.toml`, `bootstrap.sh`, empty TOMLs, minimal `app.py` that renders Home with hard-coded section names.
2. **Core** — `arch`, `shell`, `detect`, `sudo`, `symlink`, `config` loader, `logging`. Unit-test these.
3. **Salvage** — populate `config/*.toml` and `dotfiles/*` by reading `.old-root/`.
4. **Sections, simple first** — Rosetta, Homebrew, taps, brews, casks, fonts. Verify on the live machine one at a time.
5. **Sections, dotfile-touching** — Oh My Zsh, p10k, pyenv, python_tools (with the Poetry 2.x fix), direnv, dotnet, zsh_plugins, dotfiles symlinking, secrets (SSH/GPG import).
6. **Sections, GUI-affecting** — App Store via mas, VS Code extensions, Raycast (cask + browser hand-off for extensions), Terminal profile.
7. **UI polish** — checklist, progress screen, persistent header + Footer key-binding bar, Section tabs (Items / Log / Notes), syntax-highlighted RichLog, help screen, VS Code Default Dark+ theme, Nerd Font icons, progress bars.
8. **Screenshots + README** at root.

---

## Verification

End-to-end, on a real machine (this one, or ideally a fresh VM/macOS install):

1. `./bootstrap.sh` from a fresh clone — uv installs, venv created, TUI launches.
2. Home screen reflects accurate per-section status against the current system.
3. Open "Python tools" section on a machine with Poetry ≥ 2.0 — no error, Poetry step marked done, log shows the version-aware branch taken. (regression for the reported bug)
4. Run a section, hit `Esc` mid-run — current step aborts cleanly, sibling steps untouched, return to section view.
5. Re-run the same section — already-installed items show as skipped, only the unticked-now-ticked items run.
6. Sudo prompted exactly once per session, even when running multiple root-requiring sections back-to-back.
7. Dotfiles section run twice — second run is a no-op, no duplicate backups created.
8. `pytest` green for `tests/`.
9. `.old-root/` byte-identical before and after a full run (`diff -r` against a snapshot).

---

## Open / deferred

- Generating new SSH/GPG keys and registering them with GitHub — manual, account-specific. The `secrets` section restores existing keys but does not create new ones.
- Publishing as a `uv tool install`-able CLI — declined; `./bootstrap.sh` is the documented entry point. Easy to add later (one `[project.scripts]` entry) if the trade-off changes.
- Windows/Linux support — out of scope.
