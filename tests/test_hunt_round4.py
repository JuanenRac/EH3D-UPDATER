# =============================================================================
# EH3D-UPDATER - tests/test_hunt_round4.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Bug hunt: versions written with signs, spaces or digits of other scripts, patterns that can backtrack, names and paths of a manifest that climb out of the repository, and kept installations with hostile names."""
from __future__ import annotations

import json
import re
import time

import pytest

from eh3d_updater.detect import is_updater_leftover
from eh3d_updater.install import list_backups, prune_backups, restore_backup
from eh3d_updater.project_manifest import VERSION_RE, ManifestValidationError, parse_manifest
from eh3d_updater.version_parse import MAX_PATTERN_LENGTH, MAX_TEXT_LENGTH, Version, parse_version, unsafe_pattern

ARABIC = "".join(chr(0x660 + n) for n in (1, 2, 3))
FULLWIDTH = "".join(chr(0xFF10 + n) for n in (1, 2, 3))


def manifest(**changes: object) -> dict[str, object]:
    data: dict[str, object] = {
        "schema_version": "1.0",
        "ecosystem": "EH3D",
        "name": "EH3D-EXAMPLE",
        "version": "1.2.3",
        "role": "service",
        "stack": "python",
        "technologies": ["Python"],
        "deployment_target": "cm5",
        "maturity": "functional",
        "family": "Example",
        "parent": None,
        "native_version": {"file": "pyproject.toml", "pattern": r"^version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\""},
        "build": "python -m build",
        "notes": "A test-only manifest.",
    }
    data.update(changes)
    return data


def parse(**changes: object):
    return parse_manifest(json.dumps(manifest(**changes)))


# ---- versions ----

@pytest.mark.parametrize("bad", ["+1.2.3", "1.2.-3", " 1.2.3", "1.2.3 ", "1_0.2.3", f"{ARABIC}.0.0", f"0.0.{FULLWIDTH}", "1.2.3.", "1..2", "..", "1.2.3\n", "\t1.2.3", "1.2.3\x00", "0x1.2.3", "1e1.2.3", "-1.2.3"])
def test_a_version_with_a_sign_a_space_a_separator_or_other_digits_is_refused(bad):
    with pytest.raises(ValueError):
        Version.from_string(bad)


@pytest.mark.parametrize("text,want", [("0.0.0", (0, 0, 0, 0)), ("01.02.03", (1, 2, 3, 0)), ("9.9.9.9", (9, 9, 9, 9)), ("123456789012345678901234567890.0.0", (123456789012345678901234567890, 0, 0, 0))])
def test_a_version_of_plain_digits_is_read_whatever_their_size(text, want):
    v = Version.from_string(text)
    assert (v.major, v.minor, v.patch, v.build) == want


def test_versions_with_and_without_the_build_are_equal_when_the_build_is_zero_and_hash_the_same():
    a, b = Version.from_string("0.8.0"), Version.from_string("0.8.0.0")
    assert a == b and hash(a) == hash(b)
    assert len({a, b}) == 1
    assert str(a) != str(b)


def test_the_order_of_versions_is_total_and_every_comparison_agrees():
    texts = ["0.0.0", "0.7.9", "0.8.0", "0.8.0.1", "0.8.1", "1.0.0", "1.0.0.5", "10.0.0"]
    versions = [Version.from_string(t) for t in texts]
    for i, a in enumerate(versions):
        for j, b in enumerate(versions):
            assert (a < b) == (i < j) or a == b, (a, b)
            assert (a > b) == (i > j) and not (a == b) or a == b or (a > b) == (i > j), (a, b)
            assert (a <= b) == (a < b or a == b)
            assert (a >= b) == (a > b or a == b)


def test_the_number_of_a_version_is_compared_as_a_number_and_not_as_text():
    assert Version.from_string("0.0.9") < Version.from_string("0.0.10")
    assert Version.from_string("0.9.0") < Version.from_string("0.10.0")
    assert Version.from_string("2.0.0") < Version.from_string("10.0.0")


@pytest.mark.parametrize("good", ["1.2.3", "0.8.0.0", "10.20.30.40"])
def test_the_pattern_of_a_manifest_version_takes_what_a_version_is(good):
    assert VERSION_RE.fullmatch(good)


@pytest.mark.parametrize("bad", ["1.2", "1.2.3.4.5", f"{ARABIC}.0.0", f"{FULLWIDTH}.0.0", "1.2.3\n", " 1.2.3", "1.2.3 ", "a.b.c", "", "1.2.3-rc1", "+1.2.3"])
def test_the_pattern_of_a_manifest_version_refuses_what_is_not_one(bad):
    assert VERSION_RE.fullmatch(bad) is None


# ---- patterns ----

@pytest.mark.parametrize("pattern", [r"(\d+)\.(\d+)\.(\d+)", r"(\d+\.\d+\.\d+)", r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?"', r"(a|b){2}", r"(rc|beta)?", r"\(a+\)+", r"[+*]+"])
def test_the_usual_patterns_of_a_manifest_are_not_refused(pattern):
    assert unsafe_pattern(pattern) is None


@pytest.mark.parametrize("pattern", ["(a+)+$", "(?:a+)+$", "(a*)*", "(.*)*x", "(a|aa)+b", "(a|b)*c", r"(\d+|x)+", "(?:a|aa)+$"])
def test_a_pattern_that_repeats_a_repeat_or_a_group_of_alternatives_is_refused(pattern):
    assert unsafe_pattern(pattern)


def test_the_longest_pattern_is_exact_and_a_longer_one_is_refused():
    assert unsafe_pattern("a" * MAX_PATTERN_LENGTH) is None
    assert unsafe_pattern("a" * (MAX_PATTERN_LENGTH + 1))


def test_a_refused_pattern_is_never_run_so_the_search_returns_at_once():
    started = time.monotonic()
    assert parse_version("a" * 30 + "!", "(a|aa)+$") is None
    assert parse_version("a" * 30 + "!", "(a+)+$") is None
    assert time.monotonic() - started < 2.0


@pytest.mark.parametrize("pattern", [None, 5, 1.5, [], ("a",), b"x", {"major": 1, "minor": 2, "patch": 3}, {"major": r"(\d+)"}, {}, "(", "[", "(?P<", "*", r"(\d+)\.(\d+)", ""])
def test_a_pattern_that_is_wrong_gives_no_version_and_never_raises(pattern):
    assert parse_version("version = 1.2.3", pattern) is None


def test_a_pattern_of_three_groups_a_whole_version_group_and_an_optional_fourth_are_read():
    assert str(parse_version("v=1.2.3", r"(\d+)\.(\d+)\.(\d+)")) == "1.2.3"
    assert str(parse_version("v=1.2.3", r"(\d+\.\d+\.\d+)")) == "1.2.3"
    assert str(parse_version("v=0.8.0.4", r"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?")) == "0.8.0.4"
    assert str(parse_version("v=0.8.0", r"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?")) == "0.8.0"


def test_a_group_that_holds_something_that_is_not_a_version_gives_none():
    assert parse_version("v=1.2", r"(\d+\.\d+)") is None
    assert parse_version("v=a.b.c", r"([a-z.]+)") is None
    assert parse_version("v=1.2.3.4.5", r"(\d+\.\d+\.\d+\.\d+\.\d+)") is None
    assert parse_version("v=1.2.-3", r"(\S+)") is None


def test_only_the_first_million_characters_of_the_text_are_read():
    pattern = r"version=(\d+\.\d+\.\d+)"
    inside = "x" * (MAX_TEXT_LENGTH - 20) + "version=1.2.3"
    beyond = "x" * (MAX_TEXT_LENGTH + 10) + "version=1.2.3"
    assert str(parse_version(inside, pattern)) == "1.2.3"
    assert parse_version(beyond, pattern) is None


def test_a_text_of_odd_bytes_is_read_without_raising():
    assert parse_version("\x00\x00version=1.2.3\x00", r"version=(\d+\.\d+\.\d+)") is not None
    assert parse_version("", r"(\d+)\.(\d+)\.(\d+)") is None
    assert parse_version("\ud800", r"(\d+)\.(\d+)\.(\d+)") is None


# ---- the manifest ----

@pytest.mark.parametrize("name", ["../x", "a/b", "a\\b", ".hidden", "-x", "a b", "a\n", "", "  ", "\u00e9", "a" + chr(0) + "b", "..", ".", "a:b", "C:\\x", "a?b", "a#b", "a@b", "a%2e"])
def test_a_repository_name_with_a_separator_a_space_or_a_dot_at_its_start_is_refused(name):
    with pytest.raises(ManifestValidationError):
        parse(name=name)


@pytest.mark.parametrize("name", ["EH3D-DOCS", "a", "A1", "a.b_c-1", "electro-hobby-3d", "9lives", "a..b"])
def test_the_names_of_the_repositories_are_accepted(name):
    assert parse(name=name).name == name


@pytest.mark.parametrize("path", ["/etc/passwd", "\\windows", "../a", "a/../b", "a\\..\\b", "C:\\x", "C:/x", "a:b", "a\x00b", ".."])
def test_the_file_of_the_version_cannot_leave_the_repository(path):
    with pytest.raises(ManifestValidationError):
        parse(native_version={"file": path, "pattern": r"(\d+)\.(\d+)\.(\d+)"})


@pytest.mark.parametrize("path", ["pyproject.toml", "src/version.h", "a..b/c", "dir/.hidden", "src\\version.h"])
def test_a_file_of_the_version_inside_the_repository_is_accepted(path):
    assert parse(native_version={"file": path, "pattern": r"(\d+)\.(\d+)\.(\d+)"}).native_version_file == path


@pytest.mark.parametrize("path", ["/a", "\\a", "../a", "a/../b", "C:\\x", "a:b"])
def test_the_source_file_of_a_component_cannot_leave_the_repository(path):
    data = manifest(
        schema_version="1.1",
        deployment_target="mcu",
        components=[{"name": "FW", "kind": "app", "version": "0.1.0", "target": "stm32", "source": {"file": path, "prefix": "V"}}],
    )
    with pytest.raises(ManifestValidationError):
        parse_manifest(json.dumps(data))


@pytest.mark.parametrize("version", [ARABIC + ".0.0", "1.2", "1.2.3.4.5", "1.2.3\n", "v1.2.3", "1.2.3-rc1", " 1.2.3"])
def test_a_manifest_version_that_is_not_plain_digits_is_refused(version):
    with pytest.raises(ManifestValidationError):
        parse(version=version)


def test_a_min_common_that_is_not_a_version_is_ignored_and_a_version_is_kept():
    assert parse(min_common="0.2.0").min_common == "0.2.0"
    for bad in (ARABIC + ".0.0", "latest", 5, None, ["0.2.0"], "0.2"):
        assert parse(min_common=bad).min_common is None, bad


def test_a_manifest_that_is_not_an_object_or_not_json_is_a_refusal_and_not_a_crash():
    for text in ("", "[]", "null", "5", '"x"', "{", "\x00", "{}", '{"name": "a"}'):
        with pytest.raises((ManifestValidationError, ValueError)):
            parse_manifest(text)


def test_a_manifest_with_a_pattern_that_can_backtrack_is_refused_when_it_is_read():
    for pattern in ("(a+)+$", "(a|aa)+$"):
        with pytest.raises(ManifestValidationError, match="refused"):
            parse(native_version={"file": "v.txt", "pattern": pattern})


# ---- kept installations with hostile names ----

def make(workspace, *names):
    for n in names:
        (workspace / n).mkdir()


def test_a_folder_that_only_looks_like_a_backup_is_not_one(tmp_path):
    make(tmp_path, "EH3D-A.backup-1234567", "EH3D-A.backup-123456789", "EH3D-A.backup-ABCDEF12", "EH3D-A.backup-1234567g", "EH3D-A.backup-", ".backup-12345678")
    assert list_backups(tmp_path) == {}


def test_a_kept_installation_is_listed_under_its_name_and_only_for_that_name(tmp_path):
    make(tmp_path, "EH3D-A.backup-12345678", "EH3D-A.backup-abcdef01", "EH3D-B.backup-12345678", "EH3D-A")
    found = list_backups(tmp_path)
    assert sorted(found) == ["EH3D-A", "EH3D-B"]
    assert len(found["EH3D-A"]) == 2
    only = list_backups(tmp_path, "EH3D-B")
    assert list(only) == ["EH3D-B"]
    assert list_backups(tmp_path, "EH3D") == {}
    assert list_backups(tmp_path, "") == {}


def test_a_name_with_a_dot_or_a_slash_never_finds_a_backup_of_another_folder(tmp_path):
    make(tmp_path, "EH3D-A.backup-12345678")
    for name in ("..", ".", "../EH3D-A", "EH3D-A/..", "EH3D-A.backup-12345678", "EH3D-*", "EH3D-A\n"):
        assert list_backups(tmp_path, name) == {}, name


def test_a_file_named_like_a_backup_is_not_a_backup_and_a_missing_workspace_has_none(tmp_path):
    (tmp_path / "EH3D-A.backup-12345678").write_text("x", encoding="utf-8")
    assert list_backups(tmp_path) == {}
    assert list_backups(tmp_path / "missing") == {}


def test_pruning_keeps_the_newest_and_a_negative_count_keeps_none(tmp_path):
    import os

    names = [f"EH3D-A.backup-{n:08x}" for n in range(1, 5)]
    make(tmp_path, *names)
    for age, n in enumerate(names):
        os.utime(tmp_path / n, (1_000_000 + age, 1_000_000 + age))
    removed = prune_backups(tmp_path, 2, dry_run=True)
    assert sorted(p.name for p in removed) == sorted(names[:2])
    assert all((tmp_path / n).exists() for n in names), "a dry run removes nothing"
    prune_backups(tmp_path, -5)
    assert not any((tmp_path / n).exists() for n in names)


def test_restoring_with_a_name_that_climbs_out_or_a_backup_that_does_not_exist_changes_nothing(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    workspace = tmp_path / "ws"
    workspace.mkdir()
    make(workspace, "EH3D-A.backup-12345678")
    for name, backup in (("../outside", None), ("..", None), ("EH3D-B", None), ("EH3D-A", "EH3D-A.backup-ffffffff"), ("EH3D-A", "../outside"), ("EH3D-A", "")):
        result = restore_backup(name, workspace, backup=backup)
        assert result.ok is False, (name, backup)
    assert outside.is_dir() and (workspace / "EH3D-A.backup-12345678").is_dir()
    assert sorted(p.name for p in workspace.iterdir() if not p.name.startswith(".")) == ["EH3D-A.backup-12345678"]


def test_restoring_a_backup_without_a_manifest_is_refused_and_leaves_the_folders_as_they_were(tmp_path):
    make(tmp_path, "EH3D-A.backup-12345678", "EH3D-A")
    result = restore_backup("EH3D-A", tmp_path)
    assert result.ok is False
    assert sorted(p.name for p in tmp_path.iterdir() if not p.name.startswith(".")) == ["EH3D-A", "EH3D-A.backup-12345678"]


@pytest.mark.parametrize("folder,leftover", [(".git", True), (".EH3D-A.update-" + "0" * 32, True), ("EH3D-A.backup-12345678", True), ("EH3D-A", False), ("EH3D-A.backup-1234567", False), ("backup-12345678", False), ("my.backup-12345678.old", False)])
def test_what_the_updater_leaves_behind_is_told_from_a_project(folder, leftover):
    assert is_updater_leftover(folder) is leftover


def test_the_numbers_of_a_version_text_agree_with_a_plain_digits_pattern():
    for text in ("0.0.0", "1.2.3", "10.20.30.40"):
        assert re.fullmatch(r"[0-9]+(\.[0-9]+){2,3}", text) and VERSION_RE.fullmatch(text)
