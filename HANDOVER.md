# Handover — context from the first attempt

This file is a context dump for whoever picks up the project next (likely
the user starting a fresh chat). It describes what was built in the first
attempt, what worked, what didn't quite land, and the constraints that
should carry forward.

The first attempt's full source tree has been moved to `.first-attempt/`.
The legacy zsh-based tool the user is replacing still lives in
[`.old-root/automated-setup/`](.old-root/automated-setup/) as **read-only
reference**.

---

## Project purpose

Build an interactive macOS setup tool that replaces the user's older
`.old-root/automated-setup/install.sh`-based scripts. The legacy scripts
ran linearly with no resume/skip, brittle `sed`-based dotfile editing, and
no per-item control. They also broke on Poetry 2.x (see "Bugs to keep
fixed" below). The new tool should give the user finer control via a TUI.

---

## What was built in the first attempt (now in `.first-attempt/`)

- **Stack**: Python 3.9+ (macOS system Python) + Textual TUI + uv for deps
  + TOML-driven config + tomlkit + click.
- **Entry point**: `./bootstrap.sh` — installs `uv` if missing, runs
  `uv sync --python /usr/bin/python3`, then `uv run python -m macsetup`.
- **19 sections** implemented with detect/install pairs:
  Rosetta, Homebrew, Taps, Brews, Casks, Fonts, App Store, Oh My Zsh,
  Powerlevel10k, pyenv, Python tools, direnv, .NET, zsh plugins, Dotfiles,
  VS Code, Raycast, Secrets (SSH/GPG), Terminal profile.
- **Two UI modes**:
  - Home (dashboard): single-column list with live status per section
    (Nerd Font icon, name, progress bar, fraction installed).
  - First-run Wizard: step-by-step walkthrough, Run / Skip / Back per
    section, completion summary. Written after the user pointed out that
    a dashboard wasn't what they expected on first run.
- **One-time sudo modal** with background `sudo -v` keep-alive task.
- **Dotfiles approach**: symlink from `dotfiles/` in repo to `$HOME` with
  timestamped backups. **The user has since said they prefer generated
  dotfiles, not symlinks** — see "What didn't land".
- **31-test pytest suite**, all green at handover.
- **Screenshot capture script**: drives the app with Textual `Pilot` and
  saves SVGs to `assets/screenshots/`.

---

## What worked well — keep these for the next attempt

- **TOML-driven config under `config/`**: one file per section
  (`brews.toml`, `casks.toml`, `vscode_extensions.toml`, etc.) with a
  uniform `[[item]]` shape. Item-level metadata (`required`, `default`,
  `category`) drives both UI defaults and runs. Easy to edit.
- **Live system detection** via `brew list --formula`, `brew list --cask`,
  `brew tap`, `code --list-extensions`, etc. No state file to drift.
- **Section ABC** in `sections/base.py`: every section subclasses
  `Section` and implements `detect()` + `install()`. Sections cannot
  reach into each other — all cross-cutting concerns come from
  `core.{arch,shell,detect,sudo,symlink,config}`. New sections drop in
  as one file.
- **uv + system Python pattern**: the tool's own venv lives on
  `/usr/bin/python3` (always present on macOS) — pyenv versions are for
  the user's projects only, never for the tool itself.
- **Sudo keep-alive** (`core/sudo.py`): prompt-once via `sudo -S -v`,
  background `sudo -n -v` every 60s. Prevents repeated re-prompts.
- **VS Code Default Dark+ theme** in `ui/dark_plus.tcss` with the proper
  palette: `#1e1e1e` bg, `#d4d4d4` fg, `#007acc` accent, `#094771` active
  selection, `#6a9955` success, `#f44747` error, `#dcdcaa` warning.
- **Single-column layout with Nerd Font icons + progress bars** — user
  liked this.
- **`@work` decorator on action methods** that call `push_screen_wait` —
  Textual 8.x requires it (see "Bugs to keep fixed").

---

## What didn't land — informs the next attempt

- **Wizard was bolted on late**. The dashboard was built first and the
  wizard followed. The user wants a wizard-first UX: opening
  `./bootstrap.sh` should land on a step-by-step guided flow that mirrors
  the order of `.old-root/automated-setup/install.sh` quite closely.
- **Symlinked dotfiles**. The first attempt symlinks
  `dotfiles/.zshrc` → `~/.zshrc`. The user prefers the wizard to
  **generate** dotfiles directly into `$HOME` based on what they pick.
- **`Powerlevel10k` section was too thin** — just verified the brew
  formula and `~/.p10k.zsh` symlink. The user wants the section to:
  install p10k, let them run the p10k configurator interactively, then
  apply the customisations in
  `.old-root/automated-setup/configure_p10k.sh` (extensive p10k tuning
  via `sed`-based line edits).
- **`configure_p10k.sh` modifications were never ported** — the legacy
  script does a lot of fine p10k tweaks (icons, multiline prompt, custom
  segments for arch/time/dotnet/pyenv/venv). Should be ported as a
  Python function that rewrites the target lines in the freshly
  configured `~/.p10k.zsh`.
- **`~/.warprc` was never created** — the legacy script populates it
  with `dev:`, `puzzel:`, `home:`, `repo:` shortcuts for the `wd`
  plugin. Should be in the new wizard.
- **No HTML usage guide** — the user wants an HTML file generated at
  `~/MACSETUP-USAGE.html`, opened automatically on wizard completion,
  containing the notes from `.old-root/automated-setup/notes.sh` (pyenv
  usage, Poetry usage, zsh-autoswitch usage) and similar reference
  material. An "example.html" from another project of theirs will be the
  visual template (they will share it in the new chat).
- **No dedicated runtime-manager section**. The first attempt buried
  `asdf` + plugins inside `brews.toml`. The user wants a dedicated
  section for asdf-managed runtimes (dotnet, go, node, rust, etc.) so
  they can pick versions per language.
- **Reset / undo functionality** — not in the first attempt. The user
  asked for it as a non-priority feature: be able to revert what the
  wizard has done so they can iterate until it works the way they want.

---

## User-confirmed preferences (carry forward)

- **British English** in user-facing text. Professional, concise,
  active voice. Short responses unless asked for more.
- **VS Code Default Dark+ theme** for the TUI.
- **Single-column section list** on Home, not multi-pane.
- **Nerd Font icons** (MesloLG is the font the user installs).
- **Progress bars** on Home rows showing installed/total.
- **One-time sudo with background keep-alive**.
- **Never `pyenv global`** — use `pyenv local` per project or
  `pyenv shell` per session. The legacy `~/.pyenv/version` file should
  flag a warning if present.
- **uv is primary for new Python projects**, Poetry only for legacy.
- **`.old-root/` is read-only reference material** — never modified,
  moved, or deleted. Same will be true of `.first-attempt/`.
- **Visual reference**: the user shared a screenshot of
  [Posting](https://github.com/darrenburns/posting) (a Textual HTTP
  client) as a layout they like — persistent footer with live key
  bindings, syntax-highlighted log, thin header bar with title.

---

## Bugs to keep fixed

- **Poetry 2.x removed `virtualenvs.prefer-active-python`**. The legacy
  script ran `poetry config virtualenvs.prefer-active-python true` and
  `set -e` then aborted the whole script. The fix in the first attempt:
  detect Poetry version with `poetry --version`, only apply that config
  on Poetry < 2.0; on Poetry ≥ 2.0 the equivalent is
  `virtualenvs.use-poetry-python` (default `false`, which already uses
  the active Python). Any new `pyproject.toml` the tool writes must use
  `[tool.poetry.group.dev.dependencies]`, not the deprecated
  `poetry.dev-dependencies`.
- **Textual 8.x: `push_screen_wait` requires a worker context**.
  Decorate the action method with `@work` from `textual` — without it
  you get `NoActiveWorker: push_screen must be run from a worker when
  wait_for_dismiss is True`.
- **`set -e` is hostile**. Step-level errors must be caught and surfaced
  as a single row's failure, never abort sibling steps or the whole
  wizard. Only a Section can decide a failure is fatal for *dependent*
  sections (e.g. Homebrew install failing aborts Brews/Casks; one cask
  failing does not).

---

## File-level details that matter

- **Repo root path**: `/Users/lewiuberg/Repositories/setup`.
- **Legacy reference**: `.old-root/automated-setup/` —
  `install.sh` (orchestrator), `terminal.sh` (one big script with all
  zsh tooling), `brew.sh`, `brew_formulas.sh` (package lists),
  `vscode_extensions.sh`, `manual_installations.sh` (App Store URLs),
  `notes.sh` (usage notes for HTML guide), `configure_p10k.sh` (p10k
  customisation), `functions.sh` (336-line line-editor mega-utility —
  do **not** port this; use direct Python file IO instead).
- **First attempt**: `.first-attempt/` after the user moves things.
- **Apple App Store IDs**: extracted in
  `.first-attempt/config/app_store.toml` from the URLs in
  `.old-root/automated-setup/manual_installations.sh`. 15 apps total.
- **Raycast extension flow**: no programmatic install on free tier; the
  first attempt's pattern was `open <store_url>` per ticked extension
  and let the user click "Install Extension". Detection by listing
  folders under
  `~/Library/Application Support/com.raycast.macos/extensions/`.

---

## What to ask the user before re-implementing

Even with this handover, several decisions for the next attempt benefit
from explicit confirmation. Examples:

1. Should the new wizard write dotfiles directly to `$HOME`, or write to
   the repo first and then copy (giving a diff preview before commit)?
2. How should "reset / undo" work? Per-section reverse operations, or a
   single backup + restore checkpoint?
3. Should the Raycast extension list be hard-coded with sensible
   defaults, or should the user maintain it themselves?
4. Generate the HTML usage guide statically or templated (e.g. only
   include the Poetry section if Poetry was installed)?
5. The user's confirmation that Posting-style chrome (persistent footer,
   syntax-highlighted log) is still wanted.

Use `AskUserQuestion` to gather these — keep it to 2-4 questions per
batch.

---

## Files at the repo root after handover

- `HANDOVER.md` — this file.
- `NEXT_CHAT_PROMPT.md` — the prompt to paste at the start of the next
  chat. Includes the user's step list + the three additions they asked
  for (suggest improvements, analyse `.old-root/`, optional reset).
- `.old-root/` — legacy reference, read-only.
- `.first-attempt/` — first attempt's full source tree, archived.
- `.git/`, `.vscode/`, `.gitignore` — existing.
