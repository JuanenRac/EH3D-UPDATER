# =============================================================================
# EH3D-UPDATER - tests/test_main.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
from __future__ import annotations

import json
from pathlib import Path

from eh3d_updater import main as main_module
from eh3d_updater.detect import LocalDiscovery, LocalStatus
from eh3d_updater.github_client import RemoteDiscovery, RemoteStatus
from eh3d_updater.main import build_parser
from eh3d_updater.registry import ProjectEntry
from eh3d_updater.version_parse import Version


def test_status_command_parses() -> None:
    args = build_parser().parse_args(["status"])
    assert args.command == "status"
    assert args.json is False


def test_status_json_flag_parses() -> None:
    args = build_parser().parse_args(["status", "--json"])
    assert args.json is True


def test_status_json_output_is_real_machine_readable_json(monkeypatch, capsys, tmp_path) -> None:
    """Real end-to-end of cmd_status's own --json branch, against fake
    (not network/filesystem) local+remote discovery - discover_workspace/
    discover_remote_projects already have their own real coverage
    elsewhere; this test is about the CLI's own JSON shape."""
    installed_entry = ProjectEntry(name="HYDRA-UMC-SDK", stack="python", version_file="pyproject.toml", pattern="", maturity="established", role="library")
    missing_entry = ProjectEntry(name="HYDRA-UMC-GHOST", stack="python", version_file="pyproject.toml", pattern="", maturity="scaffolding", role="service")

    local_discovery = LocalDiscovery(
        projects=(
            LocalStatus(entry=installed_entry, path=tmp_path / "HYDRA-UMC-SDK", installed=True, version=Version(0, 0, 2)),
        ),
        errors=(),
    )
    remote_discovery = RemoteDiscovery(
        projects=(
            RemoteStatus(entry=installed_entry, version=Version(0, 0, 3)),
            RemoteStatus(entry=missing_entry, version=Version(1, 0, 0)),
        ),
        errors=(),
    )
    monkeypatch.setattr(main_module, "discover_workspace", lambda root: local_discovery)
    monkeypatch.setattr(main_module, "discover_remote_projects", lambda: remote_discovery)

    args = build_parser().parse_args(["status", "--json", "--workspace", str(tmp_path)])
    exit_code = args.func(args)

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["workspace_root"] == str(tmp_path)
    assert payload["total"] == 2
    assert payload["installed_count"] == 1
    assert payload["outdated_count"] == 1
    by_name = {p["name"]: p for p in payload["projects"]}
    assert by_name["HYDRA-UMC-SDK"]["installed"] is True
    assert by_name["HYDRA-UMC-SDK"]["local_version"] == "0.0.2"
    assert by_name["HYDRA-UMC-SDK"]["github_version"] == "0.0.3"
    assert by_name["HYDRA-UMC-SDK"]["state"] == "OUTDATED"
    assert by_name["HYDRA-UMC-GHOST"]["installed"] is False
    assert by_name["HYDRA-UMC-GHOST"]["local_version"] is None


# =============================================================================
# resolve_workspace_root() - real user request: remember a chosen
# workspace root across GUI launches instead of resetting to
# default_workspace_root() every time.
# =============================================================================


def test_resolve_workspace_root_uses_the_real_saved_one_when_present(monkeypatch, tmp_path) -> None:
    from eh3d_updater import settings

    real_dir = tmp_path / "saved-workspace"
    real_dir.mkdir()
    monkeypatch.setattr(settings, "get_saved_workspace_root", lambda: real_dir)
    assert main_module.resolve_workspace_root() == real_dir


def test_resolve_workspace_root_falls_back_to_the_real_default_when_nothing_saved(monkeypatch) -> None:
    from eh3d_updater import settings

    monkeypatch.setattr(settings, "get_saved_workspace_root", lambda: None)
    assert main_module.resolve_workspace_root() == main_module.default_workspace_root()


def test_install_and_update_accept_the_explicit_unavailable_validation_flag() -> None:
    parser = build_parser()
    assert parser.parse_args(["install", "X"]).accept_unavailable_validation is False
    assert parser.parse_args(["install", "X", "--accept-unavailable-validation"]).accept_unavailable_validation is True
    assert parser.parse_args(["update", "X", "--accept-unavailable-validation"]).accept_unavailable_validation is True


def test_the_flag_is_what_turns_the_acceptance_on(monkeypatch, tmp_path) -> None:
    from eh3d_updater import install, settings

    # setenv first so that the teardown restores the original state after the command sets the variable itself
    monkeypatch.setenv("EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION", "0")
    monkeypatch.setattr(settings, "load_settings", lambda: {})
    assert not install.accepts_unavailable_validation()
    args = build_parser().parse_args(["install", "NoSuchProject", "--workspace", str(tmp_path), "--accept-unavailable-validation"])
    monkeypatch.setattr(main_module, "discover_remote_projects", lambda *a, **k: RemoteDiscovery(projects=(), errors=()))
    main_module._install_or_update(args, expect_installed=False)
    assert install.accepts_unavailable_validation()


def test_a_folder_with_a_manifest_that_is_rejected_is_said_and_counted(monkeypatch, capsys, tmp_path) -> None:
    """A program on the disk whose manifest the parser rejects must not vanish from the table without a word: it is said on stderr, given in the JSON and counted."""
    entry = ProjectEntry(name="EH3D-OK", stack="python", version_file="pyproject.toml", pattern="", maturity="established", role="library")
    local_discovery = LocalDiscovery(
        projects=(LocalStatus(entry=entry, path=tmp_path / "EH3D-OK", installed=True, version=Version(0, 0, 2)),),
        errors=("EH3D-BAD: invalid manifest: unknown field 'colour'", f"workspace does not exist: {tmp_path / 'gone'}"),
    )
    monkeypatch.setattr(main_module, "discover_workspace", lambda root: local_discovery)
    args = build_parser().parse_args(["status", "--offline", "--json", "--workspace", str(tmp_path)])
    assert main_module.cmd_status(args) == 0
    captured = capsys.readouterr()
    assert "IGNORED EH3D-BAD: invalid manifest: unknown field 'colour'" in captured.err
    assert json.loads(captured.out)["ignored"] == [{"folder": "EH3D-BAD", "reason": "invalid manifest: unknown field 'colour'"}]
    # the table says how many
    args = build_parser().parse_args(["status", "--offline", "--workspace", str(tmp_path)])
    assert main_module.cmd_status(args) == 0
    assert ", 1 ignored (invalid manifest)" in capsys.readouterr().out
    # and a clean workspace has none
    clean = LocalDiscovery(projects=local_discovery.projects, errors=())
    monkeypatch.setattr(main_module, "discover_workspace", lambda root: clean)
    args = build_parser().parse_args(["status", "--offline", "--json", "--workspace", str(tmp_path)])
    main_module.cmd_status(args)
    assert json.loads(capsys.readouterr().out)["ignored"] == []
