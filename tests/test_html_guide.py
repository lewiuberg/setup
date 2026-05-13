from __future__ import annotations

from pathlib import Path

import pytest

from macsetup.core.dotfiles import render


def test_guide_renders_mise_block_when_enabled() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": True,
        "include_uv": False,
        "include_poetry": False,
        "poetry_v2": False,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [("python", "latest"), ("node", "lts")],
        "warp_shortcuts": [],
        "raycast_extensions": [],
    })
    assert "mise — polyglot runtime manager" in html
    assert "python@latest" in html
    assert "node@lts" in html
    assert "uv — Python project manager" not in html
    assert "Poetry — legacy projects" not in html


def test_guide_renders_poetry_v2_note_when_v2() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": False,
        "include_uv": False,
        "include_poetry": True,
        "poetry_v2": True,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [],
        "warp_shortcuts": [],
        "raycast_extensions": [],
    })
    assert "Poetry 2.x is installed" in html
    assert "Poetry 1.x" not in html


def test_guide_renders_poetry_v1_note_when_not_v2() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": False,
        "include_uv": False,
        "include_poetry": True,
        "poetry_v2": False,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [],
        "warp_shortcuts": [],
        "raycast_extensions": [],
    })
    assert "Poetry 1.x" in html
    assert "prefer-active-python" in html


def test_guide_skips_warp_card_when_empty() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": False,
        "include_uv": False,
        "include_poetry": False,
        "poetry_v2": False,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [],
        "warp_shortcuts": [],
        "raycast_extensions": [],
    })
    assert "Warp directory" not in html


def test_guide_includes_warp_table() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": False,
        "include_uv": False,
        "include_poetry": False,
        "poetry_v2": False,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [],
        "warp_shortcuts": [("dev", "~/Documents/Development"), ("home", "~")],
        "raycast_extensions": [],
    })
    assert "Warp directory" in html
    assert "~/Documents/Development" in html
    assert "<code>dev</code>" in html


def test_guide_includes_theme_toggle_script() -> None:
    html = render("usage_guide.html.j2", {
        "generated_at": "2026-05-12 21:00",
        "include_mise": False,
        "include_uv": False,
        "include_poetry": False,
        "poetry_v2": False,
        "include_github_auth": False,
        "include_azure_devops": False,
        "mise_runtimes": [],
        "warp_shortcuts": [],
        "raycast_extensions": [],
    })
    assert "localStorage" in html
    assert "data-theme" in html
