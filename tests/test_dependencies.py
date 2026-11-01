# =============================================================================
# EH3D-UPDATER - depends_on in the manifest and the order of installation
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import json

import pytest

from eh3d_updater.dependencies import DependencyError, install_order
from eh3d_updater.project_manifest import ManifestValidationError, parse_manifest

from test_project_manifest import valid_manifest


def manifest_with(depends_on, schema="1.1"):
    data = valid_manifest()
    data["schema_version"] = schema
    data["depends_on"] = depends_on
    return json.dumps(data)


def test_depends_on_is_a_schema_1_1_list_of_other_repositories():
    parsed = parse_manifest(manifest_with(["EH3D-COMMON", "EH3D-CORE-LIBS"]))
    assert parsed.depends_on == ("EH3D-COMMON", "EH3D-CORE-LIBS")
    assert parse_manifest(json.dumps(valid_manifest())).depends_on == ()
    with pytest.raises(ManifestValidationError, match="needs schema_version"):
        parse_manifest(manifest_with(["EH3D-COMMON"], schema="1.0"))
    for bad in ([], ["a", "a"], [3], ["../x"], ["HYDRA-UMC-EXAMPLE"]):
        with pytest.raises(ManifestValidationError):
            parse_manifest(manifest_with(bad))


def test_the_siblings_come_first_each_once():
    graph = {
        "SERVER": ["COMMON", "DRILLPRO", "ROUTEPRO"],
        "DRILLPRO": ["COMMON"],
        "ROUTEPRO": ["COMMON", "DRILLPRO"],
        "COMMON": [],
    }
    assert install_order("SERVER", graph) == ["COMMON", "DRILLPRO", "ROUTEPRO", "SERVER"]
    assert install_order("COMMON", graph) == ["COMMON"]


def test_a_missing_sibling_and_a_cycle_are_errors():
    with pytest.raises(DependencyError, match="not a project of the suite"):
        install_order("A", {"A": ["B"]})
    with pytest.raises(DependencyError, match="cycle"):
        install_order("A", {"A": ["B"], "B": ["A"]})
