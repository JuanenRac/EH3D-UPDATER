# =============================================================================
# EH3D-UPDATER - tests/test_signature_edges.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Edge cases of the signature check that need no real key: git is replaced by a fake, so the branches of `unsigned_reason` and of the trust and fingerprint rules are covered in milliseconds."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from eh3d_updater import signature
from eh3d_updater.messages import coded
from eh3d_updater.signature import SignaturePolicy, unsigned_reason

GOOD = "G\nAAAA BBBB\nCCCC DDDD\n"


def _fake_git(monkeypatch, *, verify=(0, "", ""), log=(0, GOOD, "")):
    """`git verify-commit` answers `verify` and `git log` answers `log`, each as (exit code, stdout, stderr)."""
    calls: list[list[str]] = []

    def run(cmd, **kwargs):
        calls.append(list(cmd))
        code, out, err = verify if "verify-commit" in cmd else log
        return subprocess.CompletedProcess(cmd, code, out, err)

    monkeypatch.setattr(signature.subprocess, "run", run)
    return calls


def test_a_good_trusted_signature_passes(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch)
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy()) is None


def test_a_failing_verify_commit_reports_the_last_line_git_printed(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch, verify=(1, "", "first line\nerror: no signature found\n"))
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy())
    assert reason == "candidate commit is not signed by a trusted key (error: no signature found)"


def test_a_failing_verify_commit_with_no_output_has_no_detail(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch, verify=(1, "", ""))
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy()) == "candidate commit is not signed by a trusted key"


@pytest.mark.parametrize("error", [OSError("git is missing"), subprocess.TimeoutExpired("git", 60)])
def test_git_that_cannot_run_or_hangs_is_a_reason_not_an_exception(monkeypatch, tmp_path: Path, error):
    def run(cmd, **kwargs):
        raise error

    monkeypatch.setattr(signature.subprocess, "run", run)
    assert "could not run git verify-commit" in (unsigned_reason(tmp_path, "HEAD", SignaturePolicy()) or "")


def test_a_failing_status_read_is_a_reason(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch, log=(128, "", "fatal: bad revision"))
    assert "could not read the signature status: fatal: bad revision" == unsigned_reason(tmp_path, "HEAD", SignaturePolicy())


def test_unknown_trust_is_refused_unless_the_setting_allows_it(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch, log=(0, "U\nAAAA\nAAAA\n", ""))
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy()) == coded("sig_trust_unknown", status="U")
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(accept_unknown_trust=True)) is None


@pytest.mark.parametrize("status", ["B", "X", "Y", "R", "E", "N", ""])
def test_every_status_other_than_good_is_refused_even_when_unknown_trust_is_allowed(monkeypatch, tmp_path: Path, status: str):
    _fake_git(monkeypatch, log=(0, f"{status}\nAAAA\nAAAA\n", ""))
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy(accept_unknown_trust=True))
    assert reason == coded("sig_not_good", status=status or "?")


def test_the_expected_fingerprint_matches_the_signing_key_or_the_primary_key_ignoring_spaces_and_case(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch)
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(expected_fingerprint="aaaabbbb")) is None
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(expected_fingerprint="ccccdddd")) is None


def test_another_fingerprint_is_refused_and_both_values_are_named(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch)
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy(expected_fingerprint="ffff"))
    assert reason == coded("sig_fingerprint_mismatch", expected="ffff", found="AAAA BBBB")


def test_a_fingerprint_is_required_but_git_printed_none(monkeypatch, tmp_path: Path):
    _fake_git(monkeypatch, log=(0, "G\n\n\n", ""))
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy(expected_fingerprint="ffff"))
    assert reason == coded("sig_fingerprint_mismatch", expected="ffff", found="?")


def test_the_allowed_signers_file_is_handed_to_both_git_commands(monkeypatch, tmp_path: Path):
    signers = tmp_path / "allowed_signers"
    signers.write_text("", encoding="utf-8")
    calls = _fake_git(monkeypatch)
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(allowed_signers_file=str(signers))) is None
    assert len(calls) == 2
    assert all(f"gpg.ssh.allowedSignersFile={signers}" in call for call in calls)


def test_the_default_mode_never_refuses_and_never_runs_git(monkeypatch, tmp_path: Path):
    calls = _fake_git(monkeypatch, verify=(1, "", "bad"))
    assert signature.verify_revision(tmp_path, "HEAD", SignaturePolicy()) is None
    assert calls == []


def test_the_fingerprint_is_normalised():
    assert signature._normalize_fingerprint(" AB CD\tEF ") == "abcdef"
    assert signature._normalize_fingerprint("SHA256:AbC") == "sha256:abc"
