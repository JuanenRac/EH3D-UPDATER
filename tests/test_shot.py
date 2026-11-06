# =============================================================================
# EH3D-UPDATER - tests/test_shot.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The picture mode of the window: its arguments are read and checked without a screen, and a wrong run says why and exits with 2."""
from __future__ import annotations

from pathlib import Path

import pytest

from eh3d_updater import main as main_module
from eh3d_updater import shot
from eh3d_updater.shot import ShotRequest, ShotUsageError, parse_shot_args


def test_a_size_is_two_sides_inside_the_limits() -> None:
    assert shot.parse_size("1280x720") == (1280, 720)
    assert shot.parse_size(" 800 X 600 ") == (800, 600)
    assert shot.parse_size("320x8192") == (320, 8192)
    for bad in ("", "1280", "x720", "1280x", "319x600", "800x8193", "-1x600", "1e3x600", "10x20x30", "800*600"):
        assert shot.parse_size(bad) is None, bad


def test_a_wait_is_a_whole_number_of_milliseconds_up_to_the_limit() -> None:
    assert shot.parse_wait("0") == 0
    assert shot.parse_wait(" 1500 ") == 1500
    assert shot.parse_wait("60000") == 60000
    for bad in ("", "-1", "60001", "1.5", "abc", "١٢"):
        assert shot.parse_wait(bad) is None, bad


def test_only_the_shot_option_asks_for_the_picture() -> None:
    assert shot.wants_picture(["--shot", "a.png"])
    assert shot.wants_picture(["--lang", "es", "--shot", "a.png"])
    assert not shot.wants_picture(["--cli", "status"])
    assert not shot.wants_picture([])


def test_the_picture_mode_has_its_defaults() -> None:
    request = parse_shot_args(["--shot", "start.png"])
    assert request == ShotRequest(output=Path("start.png"))
    assert request.size == shot.DEFAULT_SIZE == (1500, 900)
    assert request.wait_ms == shot.DEFAULT_WAIT_MS
    assert request.replace is False
    assert request.lang is None
    assert request.workspace is None
    assert parse_shot_args(["--shot", "B.PNG"]).output == Path("B.PNG")


def test_every_option_of_the_picture_is_read_in_any_order() -> None:
    request = parse_shot_args(["--lang", "DE", "--replace", "--size", "1280x720", "--workspace", "work", "--wait", "12", "--shot", "a.png"])
    assert request == ShotRequest(output=Path("a.png"), replace=True, size=(1280, 720), wait_ms=12, lang="de", workspace=Path("work"))


def test_every_language_of_the_window_is_accepted() -> None:
    from eh3d_updater.i18n import LANGUAGES

    assert {code for code, _label in LANGUAGES} == {"en", "es", "fr", "it", "de", "zh", "ja", "pt"}
    for code, _label in LANGUAGES:
        assert parse_shot_args(["--shot", "a.png", "--lang", code]).lang == code


def test_a_wait_of_zero_and_of_the_limit_are_allowed() -> None:
    for text, wait in (("0", 0), ("60000", 60000)):
        assert parse_shot_args(["--shot", "a.png", "--wait", text]).wait_ms == wait


@pytest.mark.parametrize(
    ("argv", "reason"),
    [
        (["--shot"], "needs a file to write"),
        (["--shot", "a.jpg"], "must end in .png"),
        (["--shot", "a.png", "--size"], "needs WIDTHxHEIGHT"),
        (["--shot", "a.png", "--size", "10x10"], "from 320 to 8192"),
        (["--shot", "a.png", "--wait"], "needs a number of milliseconds"),
        (["--shot", "a.png", "--wait", "-1"], "from 0 to 60000"),
        (["--shot", "a.png", "--wait", "60001"], "from 0 to 60000"),
        (["--shot", "a.png", "--lang"], "needs a language code"),
        (["--shot", "a.png", "--lang", "xx"], "unknown language code"),
        (["--shot", "a.png", "--workspace"], "needs a folder"),
        (["--shot", "a.png", "--workspace", " "], "needs a folder"),
        (["--size", "800x600"], "--shot needs a file to write"),
        (["--replace"], "--shot needs a file to write"),
        (["--shot", "a.png", "--nonsense"], "unknown option --nonsense"),
        (["--shot", "a.png", "--cli"], "unknown option --cli"),
        (["--shot", "a.png", "extra"], "takes no file names"),
    ],
)
def test_a_mistake_gives_its_reason(argv: list[str], reason: str) -> None:
    with pytest.raises(ShotUsageError, match=reason):
        parse_shot_args(argv)


def test_the_output_is_checked_before_the_window_opens(tmp_path: Path) -> None:
    free = ShotRequest(output=tmp_path / "new.png")
    assert shot.check_output(free) is None
    assert "does not exist" in (shot.check_output(ShotRequest(output=tmp_path / "missing" / "a.png")) or "")
    taken = tmp_path / "taken.png"
    taken.write_bytes(b"x")
    assert "give --replace" in (shot.check_output(ShotRequest(output=taken)) or "")
    assert shot.check_output(ShotRequest(output=taken, replace=True)) is None
    (tmp_path / "sub.png").mkdir()
    assert "is a folder" in (shot.check_output(ShotRequest(output=tmp_path / "sub.png", replace=True)) or "")
    assert "is not a folder" in (shot.check_output(ShotRequest(output=free.output, workspace=tmp_path / "nope")) or "")
    assert shot.check_output(ShotRequest(output=free.output, workspace=tmp_path)) is None


def test_wrong_arguments_exit_with_2_and_say_why(monkeypatch, capsys, tmp_path: Path) -> None:
    monkeypatch.setattr(main_module.sys, "argv", ["eh3d-updater", "--shot", str(tmp_path / "a.png"), "--size", "10x10"])
    assert main_module.main() == 2
    err = capsys.readouterr().err
    assert "error: --size is WIDTHxHEIGHT" in err
    assert not (tmp_path / "a.png").exists()


def test_a_run_that_cannot_write_exits_with_1_before_any_window_opens(monkeypatch, capsys, tmp_path: Path) -> None:
    existing = tmp_path / "a.png"
    existing.write_bytes(b"keep")
    monkeypatch.setattr(main_module.sys, "argv", ["eh3d-updater", "--shot", str(existing)])
    code = main_module.main()
    assert code == 1
    assert existing.read_bytes() == b"keep"
    assert "give --replace" in capsys.readouterr().err
