# =============================================================================
# EH3D-UPDATER - tests/test_signature_switch.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The visible switch for the commit-signature policy: the saved choice, the `signature` command, the text in every language and the preview of an unsigned commit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from eh3d_updater import i18n, main as main_module, settings, signature
from eh3d_updater.install import preview_update
from eh3d_updater.signature import SignaturePolicy, current_policy, describe_policy, save_policy_mode
from repo_helpers import entry, make_remote


@pytest.fixture
def saved(monkeypatch, tmp_path: Path) -> Path:
    path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", path)
    monkeypatch.delenv("EH3D_UPDATER_REQUIRE_SIGNED", raising=False)
    return path


def test_the_switch_saves_require_and_warn_and_current_policy_follows(saved: Path):
    assert current_policy().mode == "warn"
    save_policy_mode("require")
    assert current_policy().mode == "require"
    save_policy_mode("warn")
    assert current_policy().mode == "warn"
    assert json.loads(saved.read_text(encoding="utf-8"))["signature_policy"] == "warn"


def test_choosing_warn_clears_the_older_flag_that_would_keep_require_on(saved: Path):
    saved.write_text(json.dumps({"require_signed_commits": True, "lang": "pt"}), encoding="utf-8")
    assert current_policy().mode == "require"
    save_policy_mode("warn")
    assert current_policy().mode == "warn"
    assert json.loads(saved.read_text(encoding="utf-8"))["lang"] == "pt", "another saved preference must survive"


def test_a_value_that_is_not_a_mode_is_refused_and_nothing_is_saved(saved: Path):
    for bad in ("required", "on", "", "REQUIRE", None):
        with pytest.raises(ValueError):
            save_policy_mode(bad)  # type: ignore[arg-type]
    assert not saved.exists()


def test_the_environment_variable_locks_the_switch(saved: Path, monkeypatch):
    assert signature.mode_locked_by_environment() is False
    monkeypatch.setenv("EH3D_UPDATER_REQUIRE_SIGNED", "  ")
    assert signature.mode_locked_by_environment() is False
    monkeypatch.setenv("EH3D_UPDATER_REQUIRE_SIGNED", "0")
    assert signature.mode_locked_by_environment() is True


def test_describe_policy_says_the_mode_and_how_to_change_it(saved: Path, monkeypatch):
    warn = "\n".join(describe_policy(SignaturePolicy()))
    assert "warn" in warn and "signature --set require" in warn
    strict = "\n".join(describe_policy(SignaturePolicy(required=True, invalid="signature_policy='on'")))
    assert "require" in strict and "signature_policy='on'" in strict
    monkeypatch.setenv("EH3D_UPDATER_REQUIRE_SIGNED", "1")
    locked = "\n".join(describe_policy(SignaturePolicy(required=True)))
    assert "EH3D_UPDATER_REQUIRE_SIGNED" in locked and "--set" not in locked


def test_the_signature_command_shows_and_sets(saved: Path, capsys):
    assert main_module.cmd_signature(argparse.Namespace(set=None)) == 0
    assert "warn" in capsys.readouterr().out
    assert main_module.cmd_signature(argparse.Namespace(set="require")) == 0
    out = capsys.readouterr().out
    assert "now 'require'" in out and "Commit signatures: require" in out
    assert current_policy().mode == "require"


def test_the_signature_command_does_not_save_when_the_environment_decides(saved: Path, monkeypatch, capsys):
    monkeypatch.setenv("EH3D_UPDATER_REQUIRE_SIGNED", "1")
    assert main_module.cmd_signature(argparse.Namespace(set="warn")) == 1
    assert "nothing was saved" in capsys.readouterr().err
    assert not saved.exists()


def test_the_parser_accepts_only_the_two_modes():
    parser = main_module.build_parser()
    assert parser.parse_args(["signature", "--set", "require"]).set == "require"
    assert parser.parse_args(["signature"]).set is None
    with pytest.raises(SystemExit):
        parser.parse_args(["signature", "--set", "maybe"])


def test_every_language_has_the_text_of_the_switch():
    keys = ["sig_require_switch", "sig_require_off_hint", "sig_require_on_hint", "sig_locked_by_env", "log_signature_require", "log_signature_warn"]
    english = {key: i18n.TRANSLATIONS["en"][key] for key in keys}
    for code, _label in i18n.LANGUAGES:
        for key in keys:
            text = i18n.TRANSLATIONS[code][key]
            assert text.strip() and "{" not in text
            if code != "en":
                assert text != english[key], f"{key} is not translated in {code}"
    assert "EH3D_UPDATER_REQUIRE_SIGNED" in i18n.TRANSLATIONS["pt"]["sig_locked_by_env"]


def test_the_preview_of_an_unsigned_commit_says_so_in_the_default_mode(tmp_path: Path, saved: Path):
    settings.save_settings(allow_foreign_origin=True)  # the test remote is a local folder
    remote = make_remote(tmp_path)
    remote.push("1.1.0", "next", {"docs/readme.txt": "doc\n"})
    preview = preview_update(entry(), remote.workspace)
    assert preview.signature.startswith("not required, and the commit is not signed")


def test_the_preview_in_the_strict_mode_refuses_an_unsigned_commit(tmp_path: Path, saved: Path):
    settings.save_settings(allow_foreign_origin=True)  # the test remote is a local folder
    remote = make_remote(tmp_path)
    remote.push("1.1.0", "next", {"docs/readme.txt": "doc\n"})
    save_policy_mode("require")
    preview = preview_update(entry(), remote.workspace)
    assert not preview.signature.startswith("not required") and preview.signature != "accepted"


def test_status_summary_follows_the_saved_mode(saved: Path):
    assert main_module.signature_summary().startswith("Commit signatures: warn")
    save_policy_mode("require")
    assert main_module.signature_summary().startswith("Commit signatures: require")


def test_status_prints_the_summary_but_not_in_json(saved: Path, tmp_path: Path, capsys):
    args = argparse.Namespace(workspace=str(tmp_path), offline=True, notes=False, json=False, profile=None)
    main_module.cmd_status(args)
    assert "Commit signatures: warn" in capsys.readouterr().out
    args.json = True
    main_module.cmd_status(args)
    out = capsys.readouterr().out
    assert "Commit signatures" not in out and json.loads(out)["workspace_root"]
