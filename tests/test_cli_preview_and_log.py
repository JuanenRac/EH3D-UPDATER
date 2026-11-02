# =============================================================================
# EH3D-UPDATER - tests/test_cli_preview_and_log.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""`install --preview` changes nothing, and the command line writes a log file like the window does."""
from __future__ import annotations

import sys

from eh3d_updater import install as install_module
from eh3d_updater import logs
from eh3d_updater import main as main_module
from eh3d_updater.github_client import RemoteDiscovery, RemoteStatus
from eh3d_updater.main import build_parser
from eh3d_updater.registry import ProjectEntry
from eh3d_updater.version_parse import Version


def _entry(name: str, depends_on: tuple[str, ...] = ()) -> ProjectEntry:
    return ProjectEntry(name=name, stack="python", version_file="pyproject.toml", pattern="", depends_on=depends_on)


def _remote(monkeypatch, *entries: ProjectEntry) -> None:
    discovery = RemoteDiscovery(projects=tuple(RemoteStatus(entry=e, version=Version(0, 0, 1)) for e in entries), errors=())
    monkeypatch.setattr(main_module, "discover_remote_projects", lambda *a, **k: discovery)


def test_install_preview_describes_the_plan_and_touches_nothing(monkeypatch, tmp_path, capsys) -> None:
    _remote(monkeypatch, _entry("EH3D-APP", ("EH3D-LIB",)), _entry("EH3D-LIB"))
    called = []
    monkeypatch.setattr(main_module, "install_or_update", lambda *a, **k: called.append(a) or [])
    args = build_parser().parse_args(["install", "EH3D-APP", "--preview", "--workspace", str(tmp_path)])

    assert main_module.cmd_install(args) == 0

    out = capsys.readouterr().out
    assert "Preview of the installation of EH3D-APP" in out
    assert "first install EH3D-LIB" in out
    assert "https://github.com/JuanenRac/EH3D-APP" in out
    assert "Nothing was changed" in out
    assert "Installing EH3D-APP into" not in out
    assert called == []
    assert list(tmp_path.iterdir()) == []


def test_install_preview_says_when_the_build_is_skipped_and_when_signatures_are_required(monkeypatch, tmp_path, capsys) -> None:
    _remote(monkeypatch, _entry("EH3D-APP"))
    monkeypatch.setenv("EH3D_UPDATER_REQUIRE_SIGNED", "1")
    args = build_parser().parse_args(["install", "EH3D-APP", "--preview", "--no-build", "--workspace", str(tmp_path)])
    assert main_module.cmd_install(args) == 0
    out = capsys.readouterr().out
    assert "skipped (--no-build)" in out
    assert "required, an unsigned commit is refused" in out


def test_install_preview_still_refuses_an_installed_project(monkeypatch, tmp_path, capsys) -> None:
    _remote(monkeypatch, _entry("EH3D-APP"))
    (tmp_path / "EH3D-APP").mkdir()
    args = build_parser().parse_args(["install", "EH3D-APP", "--preview", "--workspace", str(tmp_path)])
    assert main_module.cmd_install(args) == 1
    assert "already exists" in capsys.readouterr().err


def test_plan_install_lists_each_step() -> None:
    from pathlib import Path

    lines = install_module.plan_install(_entry("A"), Path("/ws"), [_entry("B")], build=True)
    text = "\n".join(lines)
    assert text.index("first install B") < text.index("clone https://github.com/JuanenRac/A")
    assert "build check" in text


def test_a_cli_run_writes_a_log_with_the_command_the_output_and_the_exit_code(monkeypatch, tmp_path, capsys) -> None:
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("EH3D_UPDATER_LOG_DIR", str(log_dir))
    monkeypatch.setattr(sys, "argv", ["eh3d-updater", "--cli", "clean-backups", "--workspace", str(tmp_path), "--dry-run"])

    assert main_module.main() == 0

    [log] = list(log_dir.glob("cli_*.log"))
    text = log.read_text(encoding="utf-8")
    assert "command line: --cli clean-backups" in text
    assert "kept the newest 0 per project" in text
    assert "exit code 0" in text
    assert "kept the newest 0 per project" in capsys.readouterr().out


def test_log_file_names_the_file_and_no_log_writes_none(monkeypatch, tmp_path) -> None:
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("EH3D_UPDATER_LOG_DIR", str(log_dir))
    chosen = tmp_path / "mine" / "run.log"
    monkeypatch.setattr(sys, "argv", ["eh3d-updater", "--cli", "--log-file", str(chosen), "clean-backups", "--workspace", str(tmp_path), "--dry-run"])
    assert main_module.main() == 0
    assert chosen.is_file() and not log_dir.exists()

    monkeypatch.setattr(sys, "argv", ["eh3d-updater", "--cli", "--no-log", "clean-backups", "--workspace", str(tmp_path), "--dry-run"])
    assert main_module.main() == 0
    assert not log_dir.exists()


def test_an_error_line_goes_to_the_log_as_a_warning_and_the_failure_code_is_kept(monkeypatch, tmp_path) -> None:
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("EH3D_UPDATER_LOG_DIR", str(log_dir))
    monkeypatch.setattr(main_module, "discover_remote_projects", lambda *a, **k: RemoteDiscovery(projects=(), errors=()))
    monkeypatch.setattr(sys, "argv", ["eh3d-updater", "--cli", "install", "Nothing", "--workspace", str(tmp_path)])
    assert main_module.main() == 1
    text = next(log_dir.glob("cli_*.log")).read_text(encoding="utf-8")
    assert "WARNING Unknown ecosystem project" in text
    assert "exit code 1" in text


def test_a_log_folder_that_cannot_be_made_does_not_stop_the_command(monkeypatch, tmp_path, capsys) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv("EH3D_UPDATER_LOG_DIR", str(blocker / "logs"))
    monkeypatch.setattr(sys, "argv", ["eh3d-updater", "--cli", "clean-backups", "--workspace", str(tmp_path), "--dry-run"])
    assert main_module.main() == 0
    assert "kept the newest" in capsys.readouterr().out


def test_the_logs_of_the_command_line_are_pruned_without_touching_those_of_the_window(tmp_path) -> None:
    import os

    for index in range(5):
        path = tmp_path / f"cli_2000010{index}.log"
        path.write_text("x", encoding="utf-8")
        os.utime(path, (1000 + index, 1000 + index))
    window = tmp_path / "gui_20000101_000000.log"
    window.write_text("x", encoding="utf-8")
    with logs.cli_log(["status"], version="0", directory=tmp_path, keep=2):
        pass
    assert len(list(tmp_path.glob("cli_*.log"))) == 2
    assert window.is_file()
