# =============================================================================
# EH3D-UPDATER - tests/test_limits_and_links.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Limits on what comes from outside (answers of GitHub, patterns of a manifest) and links in carried local data."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from eh3d_updater import github_client, install
from eh3d_updater.project_manifest import ManifestValidationError, parse_manifest
from eh3d_updater.version_parse import parse_version, unsafe_pattern
from repo_helpers import manifest_text


class _Big:
    def __init__(self, size: int) -> None:
        self._size = size

    def read(self, amount: int = -1) -> bytes:
        return b"x" * (self._size if amount < 0 else min(self._size, amount))


def test_an_answer_bigger_than_the_limit_is_refused():
    with pytest.raises(RuntimeError, match="bigger than"):
        github_client._read_limited(_Big(github_client.MAX_RESPONSE_BYTES + 5))
    assert len(github_client._read_limited(_Big(1000))) == 1000


def test_a_double_whose_read_takes_no_size_still_works():
    class Plain:
        def read(self) -> bytes:
            return b"abc"

    assert github_client._read_limited(Plain()) == b"abc"


@pytest.mark.parametrize("pattern", ["(a+)+$", "(.*)*x", "(\\w+\\s?)+$", "a" * 400])
def test_a_pattern_that_can_backtrack_for_ever_or_is_huge_is_refused(pattern):
    assert unsafe_pattern(pattern)
    assert parse_version("a" * 40 + "!", pattern) is None
    data = json.loads(manifest_text("1.0.0"))
    data["native_version"]["pattern"] = pattern
    with pytest.raises(ManifestValidationError, match="refused"):
        parse_manifest(json.dumps(data))


@pytest.mark.parametrize("pattern", [r"(\d+\.\d+\.\d+)", r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', r"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?"])
def test_the_usual_patterns_are_accepted(pattern):
    assert unsafe_pattern(pattern) is None


def test_a_carried_link_stays_a_link_and_does_not_copy_what_it_points_at(tmp_path: Path):
    old, new = tmp_path / "old", tmp_path / "new"
    old.mkdir()
    new.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("not part of the project", encoding="utf-8")
    try:
        os.symlink(outside, old / "link.txt")
    except (OSError, NotImplementedError):
        pytest.skip("symbolic links cannot be created here")
    install._copy_without_replacing(str(old / "link.txt"), str(new / "link.txt"))
    assert (new / "link.txt").is_symlink()
    assert not (new / "outside.txt").exists()
