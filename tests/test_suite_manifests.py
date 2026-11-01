# =============================================================================
# EH3D-UPDATER - The manifests of the repositories of the suite and the checks of a checkout
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from eh3d_updater.install import find_build_test_script
from eh3d_updater.project_manifest import ManifestValidationError, parse_manifest
from eh3d_updater.version_parse import parse_version

from test_project_manifest import valid_manifest

WORKSPACE = Path(__file__).resolve().parents[2]


def test_hardware_bound_is_an_optional_true_or_false():
    data = valid_manifest()
    data["hardware_bound"] = False
    assert parse_manifest(json.dumps(data)).hardware_bound is False
    assert parse_manifest(json.dumps(valid_manifest())).hardware_bound is None
    data["hardware_bound"] = "no"
    with pytest.raises(ManifestValidationError, match="hardware_bound"):
        parse_manifest(json.dumps(data))


@pytest.mark.parametrize("role", ["node", "docs"])
def test_the_boards_and_the_documentation_hub_have_a_role(role):
    data = valid_manifest()
    data["role"] = role
    assert parse_manifest(json.dumps(data)).role == role


def test_a_pattern_with_one_group_holding_the_whole_version_reads_it():
    bs = chr(92)
    regex = '^version = "(' + bs + "d+" + bs + "." + bs + "d+" + bs + "." + bs + 'd+)"'
    assert str(parse_version('version = "0.0.7"', regex)) == "0.0.7"
    assert parse_version("nothing here", regex) is None


def test_a_checkout_without_build_test_is_checked_with_its_test_script(tmp_path: Path):
    name = "test.bat" if os.name == "nt" else "test.sh"
    assert find_build_test_script(tmp_path) is None
    (tmp_path / name).write_text("run the tests\n", encoding="utf-8")
    assert find_build_test_script(tmp_path) == tmp_path / name
    preferred = tmp_path / ("build-test.bat" if os.name == "nt" else "build-test.sh")
    preferred.write_text("build test\n", encoding="utf-8")
    assert find_build_test_script(tmp_path) == preferred


def test_every_manifest_of_the_suite_next_to_this_repository_is_accepted():
    found = sorted(WORKSPACE.glob("EH3D-*/eh3d.project.json"))
    if not found:
        pytest.skip("the other repositories of the suite are not next to this one")
    problems = []
    for path in found:
        try:
            parse_manifest(path.read_text(encoding="utf-8"), expected_name=path.parent.name)
        except ManifestValidationError as exc:
            problems.append(f"{path.parent.name}: {exc}")
    assert not problems, "\n".join(problems)
