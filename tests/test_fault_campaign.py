# =============================================================================
# EH3D-UPDATER - tests/test_fault_campaign.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A fault injected at a chosen step of an update, and the recovery.

The other install tests break one named step at a time. This one counts the commands an update runs against a real bare repository (the fake GitHub of the
tests), then makes a different one of them fail, by a seeded choice, in two ways (it exits with an error, or it cannot be started), and checks that the
installation is never left half updated, that nothing escapes as an exception, and that the next run without a fault finishes the update. Nothing here
touched GitHub or a real installation."""
from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

from repo_helpers import NAME, entry, git, make_remote

from eh3d_updater import install
from eh3d_updater.install import install_or_update
from eh3d_updater.messages import coded

SEED = 20240611
CASES = 4


def _version(checkout: Path) -> str:
    return json.loads((checkout / "eh3d.project.json").read_text(encoding="utf-8"))["version"]


def _head(checkout: Path) -> str:
    return git("rev-parse", "HEAD", cwd=checkout)


def _staging(workspace: Path) -> list[Path]:
    return list(workspace.glob(f".{NAME}.update-*"))


def _counting(patch) -> dict[str, int]:
    """Count the commands that `install` runs, without changing them."""
    state = {"calls": 0}
    real = install._run

    def run(cmd, cwd, *, capture_output=False):
        state["calls"] += 1
        return real(cmd, cwd, capture_output=capture_output)

    patch.setattr(install, "_run", run)
    return state


def _failing_at(patch, step: int, mode: str) -> dict[str, int]:
    """Make the `step`-th command fail: `exit` returns an error code, `missing` cannot start the program."""
    state = {"calls": 0}
    real = install._run

    def run(cmd, cwd, *, capture_output=False):
        state["calls"] += 1
        if state["calls"] == step:
            if mode == "missing":
                # what the real `_run` does when the program cannot be started
                raise install.InstallError(coded("tool_missing", tool=cmd[0], error="simulated"))
            return subprocess.CompletedProcess(cmd, 128, "" if capture_output else None, "simulated failure" if capture_output else None)
        return real(cmd, cwd, capture_output=capture_output)

    patch.setattr(install, "_run", run)
    return state


def _two_versions(tmp_path: Path):
    remote = make_remote(tmp_path, "1.0.0")
    old_head = _head(remote.checkout)
    new_head = remote.push("1.1.0", "new release")
    return remote, old_head, new_head


def _steps_of_a_clean_update(tmp_path_factory, monkeypatch) -> int:
    remote, _old, _new = _two_versions(tmp_path_factory.mktemp("count"))
    with monkeypatch.context() as patch:
        state = _counting(patch)
        results = install_or_update(entry(), remote.workspace)
    assert all(r.ok for r in results), [r.message for r in results]
    return state["calls"]


def test_a_command_that_fails_at_any_step_never_leaves_a_half_updated_installation(tmp_path_factory, monkeypatch):
    steps = _steps_of_a_clean_update(tmp_path_factory, monkeypatch)
    assert steps >= 5, f"an update runs only {steps} commands: the campaign would try nothing"
    rng = random.Random(SEED)
    chosen = sorted(rng.sample(range(1, steps + 1), min(CASES, steps)))
    for step in chosen:
        mode = rng.choice(["exit", "missing"])
        remote, old_head, new_head = _two_versions(tmp_path_factory.mktemp(f"step{step}"))
        with monkeypatch.context() as patch:
            _failing_at(patch, step, mode)
            results = install_or_update(entry(), remote.workspace)
        label = f"step {step} of {steps} ({mode})"
        assert results, label
        assert (remote.checkout / ".git").is_dir(), label
        head = _head(remote.checkout)
        assert head in (old_head, new_head), label
        assert _version(remote.checkout) == ("1.0.0" if head == old_head else "1.1.0"), label
        assert git("status", "--porcelain", cwd=remote.checkout) == "", label


def test_the_next_run_without_a_fault_finishes_an_update_that_did_not_finish(tmp_path_factory, monkeypatch):
    steps = _steps_of_a_clean_update(tmp_path_factory, monkeypatch)
    rng = random.Random(SEED + 1)
    unfinished = 0
    for step in sorted(rng.sample(range(1, steps + 1), min(CASES, steps))):
        remote, old_head, new_head = _two_versions(tmp_path_factory.mktemp(f"again{step}"))
        with monkeypatch.context() as patch:
            _failing_at(patch, step, rng.choice(["exit", "missing"]))
            install_or_update(entry(), remote.workspace)
        if _head(remote.checkout) == new_head:
            # the update was already promoted: its origin is now the official address, which the fake remote of the tests is not
            continue
        unfinished += 1
        assert _head(remote.checkout) == old_head, step
        again = install_or_update(entry(), remote.workspace)
        assert all(r.ok for r in again), (step, [r.message for r in again])
        assert _head(remote.checkout) == new_head, step
        assert _version(remote.checkout) == "1.1.0", step
        assert git("status", "--porcelain", cwd=remote.checkout) == "", step
        assert _staging(remote.workspace) == [], step
    assert unfinished > 0, "no fault stopped an update, so no recovery was tried"


def test_a_program_that_cannot_be_started_is_a_result_with_its_message_not_an_exception(tmp_path, monkeypatch):
    remote, old_head, _new = _two_versions(tmp_path)
    with monkeypatch.context() as patch:
        _failing_at(patch, 1, "missing")
        results = install_or_update(entry(), remote.workspace)
    assert len(results) == 1 and not results[0].ok and results[0].message
    assert _head(remote.checkout) == old_head
