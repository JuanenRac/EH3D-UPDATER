# =============================================================================
# EH3D-UPDATER - tests/test_trust_origin_rollback.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Three protections of an update: a signature must be trusted (status G) and
may be bound to an expected key, a checkout whose origin is not the official
repository is not updated, and an update whose health check fails is undone
by itself."""
from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from eh3d_updater import install, settings, signature
from eh3d_updater.install import clone_or_pull
from eh3d_updater.messages import localize
from eh3d_updater.registry import ProjectEntry
from eh3d_updater.signature import SignaturePolicy, current_policy, unsigned_reason
from test_install import entry, git, write_build_script, write_manifest
from test_signature import _remote_with_one_commit, _signing_key, needs_ssh_keygen


def _fake_git(monkeypatch, status: str, signing: str = "", primary: str = ""):
    real = subprocess.run

    def fake(cmd, *args, **kwargs):
        if cmd[:1] == ["git"] and "log" in cmd and any(str(c).startswith("--format=%G?") for c in cmd):
            return subprocess.CompletedProcess(cmd, 0, stdout=f"{status}\n{signing}\n{primary}\n", stderr="")
        if cmd[:1] == ["git"] and "verify-commit" in cmd:
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(signature.subprocess, "run", fake)


def test_a_good_signature_by_a_key_of_unknown_trust_is_refused(tmp_path: Path, monkeypatch):
    _fake_git(monkeypatch, "U", "ABCD 1234")
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy(True))
    assert reason is not None and "not trusted" in reason


def test_unknown_trust_can_be_accepted_by_the_setting(tmp_path: Path, monkeypatch):
    _fake_git(monkeypatch, "U", "ABCD 1234")
    settings.save_settings(signature_accept_unknown_trust=True)
    assert current_policy().accept_unknown_trust is True
    assert unsigned_reason(tmp_path, "HEAD", current_policy()) is None


@pytest.mark.parametrize("status", ["B", "X", "Y", "R", "E", "N"])
def test_any_other_status_is_refused(tmp_path: Path, monkeypatch, status):
    _fake_git(monkeypatch, status)
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(True)) is not None


def test_the_expected_fingerprint_must_match_the_signing_or_the_primary_key(tmp_path: Path, monkeypatch):
    _fake_git(monkeypatch, "G", "AAAA BBBB", "CCCC DDDD")
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(True, expected_fingerprint="aaaabbbb")) is None
    assert unsigned_reason(tmp_path, "HEAD", SignaturePolicy(True, expected_fingerprint="ccccdddd")) is None
    reason = unsigned_reason(tmp_path, "HEAD", SignaturePolicy(True, expected_fingerprint="eeee"))
    assert reason is not None and "not the expected one" in reason
    # the refusal is a translatable message
    assert "esperada" in localize("es", reason)


def test_the_fingerprint_comes_from_the_environment_or_the_settings(monkeypatch):
    settings.save_settings(signature_expected_fingerprint="AA BB cc")
    assert current_policy().expected_fingerprint == "aabbcc"
    monkeypatch.setenv("EH3D_UPDATER_EXPECTED_FINGERPRINT", "11 22")
    assert current_policy().expected_fingerprint == "1122"
    assert SignaturePolicy().expected_fingerprint is None


@needs_ssh_keygen
def test_a_real_ssh_signature_passes_with_its_fingerprint_and_fails_with_another(tmp_path: Path):
    key, allowed = _signing_key(tmp_path)
    remote = _remote_with_one_commit(tmp_path, signing_key=key)
    local = tmp_path / "local"
    git("clone", str(remote), str(local), cwd=tmp_path)
    fingerprint = subprocess.check_output(["ssh-keygen", "-lf", str(key) + ".pub"], text=True).split()[1]
    assert unsigned_reason(local, "HEAD", SignaturePolicy(True, str(allowed), None, fingerprint)) is None
    assert unsigned_reason(local, "HEAD", SignaturePolicy(True, str(allowed), None, "sha256:other")) is not None


def _remote_and_checkout(tmp_path: Path) -> tuple[Path, Path, Path]:
    remote = tmp_path / "remote.git"
    git("init", "--bare", str(remote), cwd=tmp_path)
    seed = tmp_path / "seed"
    git("clone", str(remote), str(seed), cwd=tmp_path)
    git("config", "user.email", "contract@example.invalid", cwd=seed)
    git("config", "user.name", "Contract", cwd=seed)
    write_manifest(seed, "1.0.0")
    write_build_script(seed, ok=True)
    git("add", "-A", cwd=seed)
    git("commit", "-m", "v1", cwd=seed)
    git("push", "origin", "HEAD", cwd=seed)
    local = tmp_path / entry().name
    git("clone", str(remote), str(local), cwd=tmp_path)
    write_manifest(seed, "1.1.0")
    git("add", "-A", cwd=seed)
    git("commit", "-m", "v2", cwd=seed)
    git("push", "origin", "HEAD", cwd=seed)
    return remote, seed, local


def test_a_checkout_whose_origin_is_not_the_official_repository_is_not_updated(tmp_path: Path, monkeypatch):
    settings.save_settings(allow_foreign_origin=False)
    _remote, _seed, local = _remote_and_checkout(tmp_path)
    monkeypatch.setattr(install, "github_repo_url", lambda _entry: "https://github.com/JuanenRac/" + entry().name)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=local, text=True).strip()
    result = clone_or_pull(entry(), tmp_path)
    assert not result.ok and "not the official repository" in result.message
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=local, text=True).strip() == head
    assert "oficial" in localize("es", result.message)
    with pytest.raises(install.InstallError):
        install.preview_update(entry(), tmp_path)


def test_the_setting_allows_another_origin(tmp_path: Path, monkeypatch):
    settings.save_settings(allow_foreign_origin=False)
    _remote, _seed, local = _remote_and_checkout(tmp_path)
    monkeypatch.setattr(install, "github_repo_url", lambda _entry: "https://github.com/JuanenRac/" + entry().name)
    assert install._foreign_origin(local, entry()) is not None
    settings.save_settings(allow_foreign_origin=True)
    assert install._foreign_origin(local, entry()) is None


@pytest.mark.parametrize("origin", [
    "https://github.com/JuanenRac/X",
    "https://github.com/JuanenRac/X.git",
    "git@github.com:JuanenRac/X.git",
    "ssh://git@github.com/juanenrac/X/",
    "https://user@github.com/JuanenRac/X",
])
def test_the_same_repository_in_any_notation_is_accepted(origin):
    assert install._normalized_remote(origin) == install._normalized_remote("https://github.com/JuanenRac/X")


def test_another_repository_or_host_is_not_the_same():
    official = install._normalized_remote("https://github.com/JuanenRac/X")
    for other in ("https://github.com/someone/X", "https://example.com/JuanenRac/X", "https://github.com/JuanenRac/XY"):
        assert install._normalized_remote(other) != official


def _fake_journal(monkeypatch, healthy: bool):
    class FakeJournal:
        def __init__(self, _path):
            pass

        def begin(self, *_a, **_k):
            return SimpleNamespace(promotion_id="p1")

        def advance(self, *_a):
            pass

        def complete(self, *_a):
            pass

    monkeypatch.setattr(install, "_HAS_DURABLE_JOURNAL", True, raising=False)
    monkeypatch.setattr(install, "PromotionJournal", FakeJournal, raising=False)
    monkeypatch.setattr(install, "PromotionPhase", SimpleNamespace(BACKED_UP=1, PROMOTED=2), raising=False)
    monkeypatch.setattr(install, "_check_service_health", lambda _url: (healthy, "reason"), raising=False)


def test_a_failed_health_check_puts_the_previous_installation_back(tmp_path: Path, monkeypatch):
    remote, _seed, local = _remote_and_checkout(tmp_path)
    monkeypatch.setattr(install, "github_repo_url", lambda _entry: str(remote))
    _fake_journal(monkeypatch, healthy=False)
    with_health = ProjectEntry(entry().name, "python", "pyproject.toml", r"(\d+)\.(\d+)\.(\d+)", service_port=18999, service_health_path="/health")

    result = clone_or_pull(with_health, tmp_path)

    assert not result.ok and "put back automatically" in result.message
    assert '"1.0.0"' in (local / "eh3d.project.json").read_text(encoding="utf-8"), "the previous version is the installed one again"
    names = sorted(p.name for p in tmp_path.iterdir() if p.name.startswith(entry().name + "."))
    assert any(".failed-" in n for n in names), "the failed version is kept beside it"
    assert not any(".backup-" in n for n in names), "the backup went back into place"
    assert "automáticamente" in localize("es", result.message)


def test_an_update_always_keeps_one_previous_installation_even_with_zero_configured(tmp_path: Path, monkeypatch):
    remote, _seed, _local = _remote_and_checkout(tmp_path)
    monkeypatch.setattr(install, "github_repo_url", lambda _entry: str(remote))
    settings.save_settings(backups_to_keep=0)
    results = install.install_or_update(entry(), tmp_path, build=False)
    assert all(r.ok for r in results), [r.message for r in results]
    assert install.list_backups(tmp_path, entry().name).get(entry().name), "the backup of the previous version survives"
