# =============================================================================
# EH3D-UPDATER - tests/test_dependency_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Every dependency taken from a git address is fixed to a full commit: an install must be reproducible and must not run whatever a branch holds that day."""
from __future__ import annotations

import re
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"
GIT_DEPENDENCY = re.compile(r"git\+https://[^\s\"'#]+?\.git@([^\s\"'#]+)")


def test_every_git_dependency_is_fixed_to_a_full_commit():
    text = PYPROJECT.read_text(encoding="utf-8")
    found = GIT_DEPENDENCY.findall(text)
    assert found, "the optional journal dependency is expected to come from git"
    for reference in found:
        assert re.fullmatch(r"[0-9a-f]{40}", reference), f"{reference!r} is not a full commit hash"
