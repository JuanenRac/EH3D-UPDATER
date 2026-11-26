# =============================================================================
# EH3D-UPDATER - tests/test_untrusted_input.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What arrives from GitHub or from a checkout may be damaged or hostile: it is refused with a message, one bad repository never ends the scan of the others, and the
local data of a person is carried over whatever letters its name has."""
from __future__ import annotations

import http.client
import json
import urllib.request

import pytest

from eh3d_updater import github_client
from eh3d_updater.install import _carry_over_local_data, _manifest_from_revision, _tracked_dirty_paths
from eh3d_updater.project_manifest import ManifestValidationError, parse_manifest
from eh3d_updater.version_parse import unsafe_pattern

from repo_helpers import entry, git, make_remote, manifest_text


def _with(**changes: object) -> str:
    document = json.loads(manifest_text("1.0.0"))
    document.update(changes)
    return json.dumps(document)


@pytest.mark.parametrize(
    "text",
    [
        "[" * 100_000,
        '{"a":' * 100_000,
        '{"schema_version": ' + "9" * 5000 + "}",
    ],
    ids=["nested-arrays", "nested-objects", "endless-number"],
)
def test_a_document_that_cannot_be_read_is_refused_by_name(text):
    with pytest.raises(ManifestValidationError):
        parse_manifest(text)


@pytest.mark.parametrize("version", ["1.2." + "9" * 5000, "9" * 10 + ".0.0", "1.0.0." + "1" * 10])
def test_a_version_with_a_number_too_long_is_refused(version):
    with pytest.raises(ManifestValidationError, match="version"):
        parse_manifest(_with(version=version))


def test_a_version_of_nine_digits_is_still_read():
    assert parse_manifest(_with(version="999999999.0.0")).version == "999999999.0.0"


@pytest.mark.parametrize("pattern", [r"((a+))+$", r"(?:(a*))*b", r"((?:\d+)?)+x", r"((a|aa))+$", r"(a{1,})+$", r"(x(\w+)y){3}"])
def test_extra_parentheses_do_not_hide_a_pattern_that_can_backtrack(pattern):
    assert unsafe_pattern(pattern)


@pytest.mark.parametrize(
    "pattern",
    [
        r"(\d+)\.(\d+)\.(\d+)",
        r"(\d+\.\d+\.\d+(?:\.\d+)?)",
        r"^version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\"",
        r"([+*|(]+)",
        r"\((\d+)\)+",
        r"[])+](\d)+",
        r"(?:a|b)(\d{1,3})",
        r"(\d{1,3}\.){3}",
    ],
)
def test_the_usual_patterns_are_still_accepted(pattern):
    assert unsafe_pattern(pattern) is None


class _Cut:
    headers = None

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def read(self, *_size):
        raise http.client.IncompleteRead(b"{")


def test_an_answer_cut_in_half_is_asked_again_and_then_raised():
    calls = []

    def opener(request, timeout):
        calls.append(1)
        return _Cut()

    with pytest.raises(http.client.IncompleteRead):
        github_client._urlopen_with_retries(urllib.request.Request("https://example.invalid/"), timeout=1, max_attempts=3, opener=opener, sleep=lambda _s: None)
    assert len(calls) == 3


def test_one_cut_manifest_does_not_end_the_discovery_of_the_others(monkeypatch):
    def fetch(request, **_options):
        raise http.client.IncompleteRead(b"{")

    monkeypatch.setattr(github_client, "_urlopen_with_retries", fetch)
    with pytest.raises(RuntimeError, match="EH3D-EXAMPLE: manifest lookup failed"):
        github_client._fetch_discovered_manifest("owner", "EH3D-EXAMPLE", "main")


def test_local_files_with_letters_of_any_language_are_carried_over(tmp_path):
    remote = make_remote(tmp_path)
    names = ["ajustes-ni\u00f1o.json", "\u8a2d\u5b9a.txt", "pr\u00e9r\u00e9glage \u00fcber.cfg"]
    for name in names:
        (remote.checkout / name).write_text("mine", encoding="utf-8")
    staging = tmp_path / "staging"
    staging.mkdir()
    _carry_over_local_data(remote.checkout, staging)
    for name in names:
        assert (staging / name).read_text(encoding="utf-8") == "mine"


def test_a_changed_file_with_a_name_in_another_language_is_reported_by_its_name(tmp_path):
    remote = make_remote(tmp_path)
    name = "calibraci\u00f3n.txt"
    remote.push("1.0.0", "a file", {name: "one"})
    git("pull", "--ff-only", cwd=remote.checkout)
    (remote.checkout / name).write_text("two", encoding="utf-8")
    assert _tracked_dirty_paths(remote.checkout) == [name]


def test_the_manifest_of_a_revision_is_read_as_utf8(tmp_path):
    remote = make_remote(tmp_path)
    notes = "\u30de\u30cb\u30d5\u30a7\u30b9\u30c8 \u00c1\u00cd\u00dd"
    document = json.loads(manifest_text("1.0.1"))
    document["notes"] = notes
    (remote.checkout / "eh3d.project.json").write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    git("-c", "user.name=Contract", "-c", "user.email=contract@example.invalid", "commit", "-am", "notes", cwd=remote.checkout)
    assert _manifest_from_revision(remote.checkout, "HEAD", entry()).notes == notes
