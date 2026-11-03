# =============================================================================
# EH3D-UPDATER - tests/test_dependencies_windows.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The windows install the sibling repositories a project needs, first and in order, like the command line does."""
from __future__ import annotations

from pathlib import Path

from eh3d_updater import install
from eh3d_updater.install import InstallResult, install_with_dependencies
from eh3d_updater.registry import ProjectEntry


def _entry(name: str, *needs: str) -> ProjectEntry:
    return ProjectEntry(name, "rust", "Cargo.toml", r"(\d+)\.(\d+)\.(\d+)", depends_on=tuple(needs))


def test_missing_siblings_are_installed_first_in_dependency_order(tmp_path: Path, monkeypatch):
    known = {e.name: e for e in (_entry("EH3D-APP", "EH3D-MID"), _entry("EH3D-MID", "EH3D-COMMON"), _entry("EH3D-COMMON"))}
    done: list[str] = []

    def fake(entry, root, **_kw):
        done.append(entry.name)
        (root / entry.name).mkdir()
        return [InstallResult(True, entry.name)]

    monkeypatch.setattr(install, "install_or_update", fake)
    results = install_with_dependencies(known["EH3D-APP"], tmp_path, known)
    assert done == ["EH3D-COMMON", "EH3D-MID", "EH3D-APP"] and all(r.ok for r in results)


def test_an_installed_sibling_is_left_alone_and_a_failure_stops_the_run(tmp_path: Path, monkeypatch):
    known = {e.name: e for e in (_entry("EH3D-APP", "EH3D-MID", "EH3D-COMMON"), _entry("EH3D-MID"), _entry("EH3D-COMMON"))}
    (tmp_path / "EH3D-COMMON").mkdir()
    done: list[str] = []

    def failing(entry, root, **_kw):
        done.append(entry.name)
        return [InstallResult(False, "boom")]

    monkeypatch.setattr(install, "install_or_update", failing)
    results = install_with_dependencies(known["EH3D-APP"], tmp_path, known)
    assert done == ["EH3D-MID"] and not results[-1].ok


def test_an_unknown_dependency_is_a_failed_result_not_a_crash(tmp_path: Path):
    app = _entry("EH3D-APP", "EH3D-NOPE")
    (result,) = install_with_dependencies(app, tmp_path, {"EH3D-APP": app})
    assert not result.ok and "EH3D-NOPE" in result.message
