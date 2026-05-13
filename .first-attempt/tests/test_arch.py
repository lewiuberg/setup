from pathlib import Path
from unittest.mock import patch

import pytest

from macsetup.core import arch as arch_mod


def test_arm64_detect():
    with patch("platform.machine", return_value="arm64"):
        assert arch_mod.detect() is arch_mod.Arch.ARM64


def test_x86_64_detect():
    with patch("platform.machine", return_value="x86_64"):
        assert arch_mod.detect() is arch_mod.Arch.X86_64


def test_i386_treated_as_x86_64():
    with patch("platform.machine", return_value="i386"):
        assert arch_mod.detect() is arch_mod.Arch.X86_64


def test_unsupported_arch_raises():
    with patch("platform.machine", return_value="ppc"):
        with pytest.raises(RuntimeError):
            arch_mod.detect()


def test_brew_prefix_arm():
    assert arch_mod.brew_prefix(arch_mod.Arch.ARM64) == Path("/opt/homebrew")


def test_brew_prefix_intel():
    assert arch_mod.brew_prefix(arch_mod.Arch.X86_64) == Path("/usr/local")


def test_brew_bin_arm():
    assert arch_mod.brew_bin(arch_mod.Arch.ARM64) == Path("/opt/homebrew/bin/brew")
