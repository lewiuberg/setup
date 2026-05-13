# macsetup wizard — implementation plan

## Context

The user is restarting a macOS dev-environment setup project. The first attempt (now archived at `.first-attempt/`) was a Python+Textual TUI that landed 19 sections and 31 passing tests, but the wizard was "bolted on late" — the UX wasn't wizard-first, and a Poetry 2.x breaking change halted progress. The legacy plain-shell scripts in `.old-root/automated-setup/` worked end-to-end 3-5 years ago but contain stale package URLs, deprecated taps (`homebrew/cask-fonts`), and choices that have better modern equivalents (mise > pyenv + asdf + zsh-autoswitch-virtualenv).

This plan rebuilds the wizard from scratch using the same stack (Python + Textual + uv + TOML) but with a **plan-then-execute** UX modelled on the legacy `install.sh` order, modern tooling (mise, gh CLI, brew cask for fonts), and dotfiles generated directly into `$HOME` rather than symlinked from the repo.

Reset/undo is deferred to post-MVP per the user's request.

## Confirmed design decisions

| Area | Decision |
|---|---|
| Stack | Python 3.11+, Textual TUI, uv-managed project, TOML config files |
| Project layout | New `src/macsetup/` — fresh code, **not** reused from `.first-attempt/`. That folder stays as read-only reference. |
| Entry | `./bootstrap.sh` → installs uv → `uv sync` → `uv run python -m macsetup` |
| UX model | **Plan-then-execute.** Two-pane TUI: section list (left) + detail/checkboxes (right). User ticks what to include across all sections, then hits `[Run plan]` to execute top-to-bottom. |
| Theme | VS Code Dark+ palette: `#1e1e1e` bg, `#d4d4d4` fg, `#007acc` accent. Nerd Font icons. Persistent footer with key bindings. |
| Version manager | **mise** for everything (Python, dotnet, go, node, rust). Replaces pyenv + asdf + zsh-autoswitch-virtualenv. Configurable to use python-build backend if PyPy/anaconda needed later. |
| Fonts | `brew install --cask` (Meslo Nerd Font + Fira Code + JetBrains Mono baseline). No deprecated taps. |
| Dotfiles | **Generated** to `$HOME` from Jinja2 templates. Existing files backed up to `~/.dotfile-backups/<timestamp>/` before fresh write. |
| Auth | `gh auth login` for GitHub (handles SSH key + upload + credential helper + signing). Dedicated Azure DevOps step (copy SSH key, open DevOps SSH-keys page in browser). |
| VS Code | Open VS Code → user confirms Settings Sync is signed in → wizard compares `code --list-extensions` against baseline TOML → offers to install any missing. |
| Sudo | Prompt **once** at the start of the execute phase, keep alive in background (legacy `install.sh` pattern) — never re-prompt mid-run. |
| Interactive breaks | Pause inline. Modal explains what's about to happen, wizard yields the terminal to the subprocess (p10k configurator, gh auth, etc.), resumes on exit. |
| List source | `config/*.toml` shipped with curated defaults, user edits TOML to customise. |
| HTML guide | Jinja2-templated by selections (Poetry section only if Poetry was installed, etc.). Visual style mimics `example.html` (CSS custom properties, dark/light toggle, monospace, cards/badges/info-boxes). Written to `~/MACSETUP-USAGE.html` and auto-opened on completion. |
| Reset/undo | **Out of scope for MVP.** Plan a clean extension point but don't build it. |

## Wizard step flow

**Phase 0 — Bootstrap (runs before TUI)**
1. Verify zsh is the user's login shell. Create empty `~/.zprofile` and `~/.zshrc` if absent.
2. Prompt: "Install Rosetta 2?" (only on Apple Silicon; via `softwareupdate --install-rosetta`).
3. Detect arch (`arm64` vs `x86_64`) for downstream brew prefix decisions.

**Phase 1 — Plan (TUI section browser)**
User ticks per-section and per-item. No installs run.

| # | Section | Notes |
|---|---|---|
| 1 | Homebrew | Install if absent (`/bin/bash -c "$(curl …install.sh)"`), then `brew doctor` + `brew update`. |
| 2 | Taps | Per-item checklist from `config/taps.toml`. Skip-all toggle. |
| 3 | Brew formulae | Per-item from `config/brews.toml`. |
| 4 | Brew casks | Per-item from `config/casks.toml`. |
| 5 | Fonts | Per-item from `config/fonts.toml` (Meslo Nerd Font, Fira Code, JetBrains Mono, …). All via cask. |
| 6 | App Store (mas) | Per-item from `config/mas_apps.toml`. Requires user signed in to App Store; wizard checks `mas account` first. |
| 7 | Oh My Zsh | Idempotent install (check `~/.oh-my-zsh` first). |
| 8 | Powerlevel10k | Install p10k → run `p10k configure` interactively → apply custom mods from `configure_p10k.sh` via Jinja2 template, not sed. |
| 9 | Zsh plugins | zsh-syntax-highlighting, zsh-autosuggestions only (autoswitch dropped). `~/.warprc` generated with `dev:`/`puzzel:`/`home:`/`repo:` shortcuts. |
| 10 | mise + runtimes | Install mise → per-runtime checklist from `config/mise_runtimes.toml` (python, node, go, rust, dotnet). |
| 11 | Python tools | uv (always recommended), Poetry (opt-in, legacy). Apply version-aware Poetry config (see "Poetry fix" below). |
| 12 | Raycast | Install Raycast cask. Per-item extension list from `config/raycast_extensions.toml`. Each extension: open Raycast Store URL in browser one by one. |
| 13 | Manual app installs | Per-item from `config/manual_apps.toml`. mas where possible, otherwise open download URL. |
| 14 | VS Code | Open VS Code → confirm sync → check `code --list-extensions` against `config/vscode_extensions.toml` → offer missing. |
| 15 | Dotfiles | Generate `~/.zshrc`, `~/.zprofile`, `~/.p10k.zsh` (if user opted to overwrite), `~/.warprc`. Back up existing files to `~/.dotfile-backups/<timestamp>/`. |
| 16 | GitHub auth | `gh auth login` (interactive). |
| 17 | Azure DevOps auth | Opt-in. Copy SSH public key to clipboard via `pbcopy`, open DevOps SSH-keys page in browser. |
| 18 | HTML usage guide | Generate `~/MACSETUP-USAGE.html` from Jinja2 template using the plan's selections. Open via `open` command. |

**Phase 2 — Execute**
- Prompt for sudo once → start background keep-alive (`while true; sudo -n true; sleep 60`).
- Iterate selected sections top-to-bottom. For each: detect-then-install, stream stdout to the log pane, mark `[done]`/`[skipped]`/`[failed]`.
- Interactive sections pause inline: modal → yield TTY → subprocess → resume on exit code.
- On failure, ask: retry / skip / abort. Don't auto-rollback.

**Phase 3 — Finish**
- Generate and open the HTML guide.
- Show a summary screen: counts of installed/skipped/failed, path to backups, link to guide.

## Key technical specifics

**Poetry 2.x version-aware config:**
- `poetry --version` → parse semver.
- If `< 2.0`: `poetry config virtualenvs.prefer-active-python true`.
- If `>= 2.0`: `poetry config virtualenvs.use-poetry-python false` (or simply skip — `false` is already default).
- Any generated `pyproject.toml` boilerplate uses `[tool.poetry.group.dev.dependencies]`, not the deprecated `poetry.dev-dependencies`.

**ZSHRC architecture block** (preserve verbatim from [.old-root/automated-setup/terminal.sh:27-39](.old-root/automated-setup/terminal.sh#L27-L39)) — handles Rosetta 2 brew paths cleanly. Goes into the generated `~/.zshrc` template.

**`~/.warprc`** (preserve from [.old-root/automated-setup/terminal.sh:234-250](.old-root/automated-setup/terminal.sh#L234-L250)) — `wd` shortcuts. Path values should come from a small TOML, not hard-coded.

**Aliases** — port the useful subset from [.old-root/automated-setup/terminal.sh:457-472](.old-root/automated-setup/terminal.sh#L457-L472). Drop `back` (non-standard).

**`.old-root/uv-python-symlink.sh`** is no longer needed — mise + uv together provide the same Python availability cleanly.

**p10k customisation** — move from sed-based edits to a Jinja2 template seeded by the user's `p10k configure` output. Brittle sed approach in legacy `configure_p10k.sh` is the failure mode to avoid.

## Critical files (new code)

```
/Users/lewiuberg/Repositories/setup/
├── bootstrap.sh                          # uv install + uv sync + run
├── pyproject.toml                        # Python 3.11+, textual, jinja2, tomli, pytest
├── config/
│   ├── taps.toml
│   ├── brews.toml
│   ├── casks.toml
│   ├── fonts.toml
│   ├── mas_apps.toml
│   ├── mise_runtimes.toml
│   ├── raycast_extensions.toml
│   ├── manual_apps.toml
│   └── vscode_extensions.toml
├── src/macsetup/
│   ├── __main__.py                       # Textual app entry
│   ├── app.py                            # main App class
│   ├── core/
│   │   ├── arch.py                       # arm64/x86_64 detection
│   │   ├── sudo.py                       # one-shot prompt + keep-alive
│   │   ├── shell.py                      # subprocess wrappers, TTY-yielding interactive helper
│   │   ├── detect.py                     # is_installed() helpers per tool
│   │   ├── config.py                     # TOML loaders
│   │   ├── dotfiles.py                   # backup + generate from Jinja2
│   │   └── logging.py                    # stream to TUI log pane
│   ├── sections/                         # one file per section, ~18 files
│   │   ├── base.py                       # Section ABC: detect() / plan_widget() / execute()
│   │   ├── rosetta.py
│   │   ├── homebrew.py
│   │   ├── taps.py
│   │   ├── brews.py
│   │   ├── casks.py
│   │   ├── fonts.py
│   │   ├── mas.py
│   │   ├── oh_my_zsh.py
│   │   ├── powerlevel10k.py
│   │   ├── zsh_plugins.py
│   │   ├── mise.py
│   │   ├── python_tools.py
│   │   ├── raycast.py
│   │   ├── manual_apps.py
│   │   ├── vscode.py
│   │   ├── dotfiles.py
│   │   ├── github_auth.py
│   │   ├── azure_devops.py
│   │   └── html_guide.py
│   ├── screens/
│   │   ├── plan.py                       # the two-pane planner
│   │   ├── executor.py                   # runs the plan, shows log
│   │   ├── interactive_modal.py          # yields TTY for p10k/gh/etc.
│   │   └── summary.py
│   ├── templates/
│   │   ├── zshrc.j2
│   │   ├── zprofile.j2
│   │   ├── warprc.j2
│   │   ├── p10k.zsh.j2
│   │   └── usage_guide.html.j2           # mimics example.html
│   └── ui/
│       ├── dark_plus.tcss
│       └── widgets.py
└── tests/
    ├── test_config.py
    ├── test_dotfiles.py
    ├── test_detect.py
    └── test_sections/...
```

## Files to read closely during implementation (reference, not edit)

- [.old-root/automated-setup/install.sh](.old-root/automated-setup/install.sh) — section order, sudo keep-alive pattern.
- [.old-root/automated-setup/terminal.sh](.old-root/automated-setup/terminal.sh) — ZSHRC blocks, aliases, .warprc, plugin install commands.
- [.old-root/automated-setup/notes.sh](.old-root/automated-setup/notes.sh) — content for the HTML guide.
- [.old-root/automated-setup/configure_p10k.sh](.old-root/automated-setup/configure_p10k.sh) — what custom p10k segments to template.
- [example.html](example.html) — visual reference for the generated HTML guide (CSS variables, dark/light toggle, cards, badges, monospace).
- [.first-attempt/src/macsetup/](.first-attempt/src/macsetup/) — patterns worth re-deriving (section ABC, sudo keep-alive, TOML schema) without literal reuse.

## Implementation order (PR-sized chunks)

1. **Scaffold + config loader** — `pyproject.toml`, `bootstrap.sh`, empty Textual app, TOML loader, one stub section to prove the pipeline. Tests for config loader.
2. **Plan screen** — two-pane layout with section list + detail. Hard-coded sections, no execution. Theme.
3. **Executor + sudo** — running a single section, sudo prompt + keep-alive, log streaming.
4. **Core sections** — Homebrew, taps, brews, casks, fonts. Detect-then-install everywhere.
5. **Shell sections** — Oh My Zsh, zsh plugins, mise.
6. **Powerlevel10k + dotfile generation** — interactive yield for `p10k configure`, then Jinja2 templates for `~/.zshrc`/`~/.zprofile`/`~/.p10k.zsh`/`~/.warprc` with backups.
7. **Python tools** — uv + Poetry with the 2.x-aware fix.
8. **Auth** — gh CLI flow + Azure DevOps step.
9. **VS Code** — open + sync confirm + extension diff.
10. **Raycast + mas + manual apps**.
11. **HTML guide** — Jinja2 template that mimics `example.html`, templated by selections, auto-open.
12. **Polish** — summary screen, key bindings, error recovery prompts, dry-run mode.

## Verification

- **Unit tests** (`uv run pytest`):
  - Config TOML loaders parse the shipped files.
  - Dotfile generator produces stable output from fixture TOML inputs (snapshot tests).
  - Version-aware Poetry config picks the right command per parsed version.
  - `detect.is_brew_installed()` etc. mocked-subprocess unit tests.
- **End-to-end manual**:
  - Run `./bootstrap.sh` on the user's machine (current state has Homebrew/most tools already → exercises the "skip if already installed" paths).
  - Run on a fresh-ish account (or test container) → exercises the install paths.
  - Re-run after success → every section should report "already installed", no destructive changes.
  - Diff `~/.dotfile-backups/<timestamp>/` against current `$HOME` to confirm backups capture pre-wizard state.
  - Confirm `~/MACSETUP-USAGE.html` opens, contains only sections matching what was installed, styled like `example.html`.
- **Idempotency check**: every section's `execute()` must short-circuit when `detect()` returns true. Add a `--dry-run` flag that runs detect-only and prints what would happen.

## Open items deferred

- Reset/undo (per user, post-MVP).
- 1Password SSH agent integration (not requested; can be added as opt-in section later).
- direnv (skipped; mise covers the venv-switching use case).
- PyPy/anaconda support via mise (default install uses python-build-standalone; document the python-build override in the HTML guide).
