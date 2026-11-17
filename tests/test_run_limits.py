# =============================================================================
# EH3D-UPDATER - tests/test_run_limits.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A command that never ends must not hold the update for ever: it is stopped after the limit of the settings, a git that wants a password fails at once,
and a limit of 0 means no limit."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from eh3d_updater import install, settings
from eh3d_updater.i18n import LANGUAGES
from eh3d_updater.messages import CodedText, localize


def _python(code: str) -> list[str]:
    return [sys.executable, "-c", code]


def test_a_command_that_runs_past_the_limit_is_stopped_and_the_update_refused(tmp_path: Path):
    started = time.monotonic()
    with pytest.raises(install.InstallError) as caught:
        install._run(_python("import time; time.sleep(60)"), tmp_path, capture_output=True, timeout=1)
    assert time.monotonic() - started < 30
    message = caught.value.args[0]
    assert isinstance(message, CodedText) and message.code == "timed_out"
    assert message.params["seconds"] == 1


def test_the_stopped_command_takes_its_children_with_it(tmp_path: Path):
    marker = tmp_path / "child-alive"
    child = f"import time, pathlib; time.sleep(3); pathlib.Path({str(marker)!r}).write_text('alive')"
    parent = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(60)"
    with pytest.raises(install.InstallError):
        install._run(_python(parent), tmp_path, capture_output=True, timeout=1)
    time.sleep(5)
    assert not marker.exists(), "the child of the stopped command went on running"


def test_a_command_within_the_limit_returns_its_output_and_a_limit_of_zero_means_none(tmp_path: Path):
    quick = install._run(_python("print('done')"), tmp_path, capture_output=True, timeout=30)
    assert quick.returncode == 0 and quick.stdout.strip() == "done"
    none = install._run(_python("print('no limit')"), tmp_path, capture_output=True, timeout=0)
    assert none.returncode == 0 and none.stdout.strip() == "no limit"
    failing = install._run(_python("import sys; sys.exit(3)"), tmp_path, capture_output=True, timeout=30)
    assert failing.returncode == 3


def test_git_never_waits_for_a_password(tmp_path: Path):
    seen = install._run(_python("import os; print(os.environ.get('GIT_TERMINAL_PROMPT'))"), tmp_path, capture_output=True, timeout=30)
    assert seen.stdout.strip() == "0"


def test_the_limits_come_from_the_settings_with_safe_defaults(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_PATH", tmp_path / "settings.json")
    assert settings.get_timeout("git_timeout_s") == 600
    assert settings.get_timeout("build_timeout_s") == 1800
    (tmp_path / "settings.json").write_text(json.dumps({"git_timeout_s": 5, "build_timeout_s": 0}), encoding="utf-8")
    assert settings.get_timeout("git_timeout_s") == 5
    assert settings.get_timeout("build_timeout_s") is None
    for wrong in ("soon", -1, 100000, True, None):
        (tmp_path / "settings.json").write_text(json.dumps({"git_timeout_s": wrong}), encoding="utf-8")
        assert settings.get_timeout("git_timeout_s") == 600
    assert install._timeout_for(["git", "fetch"]) == 600.0
    assert install._timeout_for(["bash", "build-test.sh"]) == 1800.0


def test_every_language_tells_which_command_was_stopped():
    text = CodedText("timed_out", {"tool": "git", "seconds": 600})
    for lang, _name in LANGUAGES:
        shown = localize(lang, text)
        assert "git" in shown and "600" in shown, lang
