# =============================================================================
# EH3D-UPDATER - The picture mode of the window: shot.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The picture mode of the window (`--shot FILE.png`): what is asked for, read and checked without a screen.

The window opens at the size asked, waits a number of milliseconds so that the drawing is complete, saves what it drew as a PNG file and closes by itself.
In this mode the window keeps no settings and writes no log, so a run leaves nothing of the person's changed. This module is plain Python (no Qt), so
the command line can read and refuse the arguments on a machine without a screen; `qt_gui.launch_qt_shot` takes the picture.

Exit codes of the picture mode: 0 when the file was written, 1 when it was not, 2 for wrong arguments.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .i18n import LANGUAGES

#: The smallest side of the window of a picture, in pixels.
SIZE_MIN = 320
#: The largest side of the window of a picture, in pixels.
SIZE_MAX = 8192
#: The size of the window of a picture when `--size` is not given (the one the window opens with).
DEFAULT_SIZE = (1500, 900)
#: The milliseconds the window is given to draw before the picture is taken, when `--wait` is not given.
DEFAULT_WAIT_MS = 1500
#: The most milliseconds `--wait` may ask for.
WAIT_MAX_MS = 60000
#: The milliseconds after the wait in which the picture may still be taken; after them the run fails.
PATIENCE_MS = 30000

EXIT_WRITTEN = 0
EXIT_FAILED = 1
EXIT_USAGE = 2

_OPTIONS_WITH_VALUE = ("--shot", "--size", "--wait", "--lang", "--workspace")


class ShotUsageError(ValueError):
    """The arguments of the picture mode are wrong; the message is the reason."""


@dataclass(frozen=True)
class ShotRequest:
    """What the picture mode was asked for."""

    output: Path
    #: True when a file that exists may be replaced; otherwise it is an error.
    replace: bool = False
    #: The size of the window in pixels, width and height.
    size: tuple[int, int] = DEFAULT_SIZE
    #: The milliseconds the window is given to draw before the picture is taken.
    wait_ms: int = DEFAULT_WAIT_MS
    #: The language of the window (one of the codes of the language list); None takes English.
    lang: str | None = None
    #: The workspace to show; None shows an empty one, so that no folder of the person is in the picture.
    workspace: Path | None = None


def wants_picture(argv: list[str]) -> bool:
    """Whether the arguments ask for the picture mode."""
    return "--shot" in argv


def parse_size(text: str) -> tuple[int, int] | None:
    """Reads a size written `WIDTHxHEIGHT` (`1280x720`, also with a capital X), each side between SIZE_MIN and SIZE_MAX."""
    width, separator, height = text.strip().lower().partition("x")
    if not separator:
        return None
    try:
        sides = (int(width.strip()), int(height.strip()))
    except ValueError:
        return None
    if not all(SIZE_MIN <= side <= SIZE_MAX for side in sides):
        return None
    return sides


def parse_wait(text: str) -> int | None:
    """Reads the milliseconds of `--wait`: a whole number from 0 to WAIT_MAX_MS."""
    text = text.strip()
    if not text.isascii() or not text.isdigit():
        return None
    value = int(text)
    return value if value <= WAIT_MAX_MS else None


def parse_shot_args(argv: list[str]) -> ShotRequest:
    """Reads the arguments of the picture mode: `--shot FILE.png`, `--size WxH`, `--wait MS`, `--lang CODE`, `--workspace DIR` and `--replace`.

    Raises ShotUsageError, with the reason, for a mistake: an option without its value, a name that does not end in .png, a size or a wait out of range,
    a language the window does not have, an option that is not known or a bare argument.
    """
    output: str | None = None
    size: tuple[int, int] | None = None
    wait: int | None = None
    lang: str | None = None
    workspace: str | None = None
    replace = False
    items = list(argv)
    index = 0
    while index < len(items):
        arg = items[index]
        index += 1
        if arg == "--replace":
            replace = True
            continue
        if arg not in _OPTIONS_WITH_VALUE:
            if arg.startswith("--"):
                raise ShotUsageError(f"unknown option {arg}")
            raise ShotUsageError(f"{arg}: the picture mode takes no file names; give the file to write after --shot")
        if index >= len(items):
            raise ShotUsageError(_missing_value(arg))
        value = items[index]
        index += 1
        if arg == "--shot":
            if not value.lower().endswith(".png"):
                raise ShotUsageError("--shot writes a PNG file: the name must end in .png")
            output = value
        elif arg == "--size":
            size = parse_size(value)
            if size is None:
                raise ShotUsageError(f"--size is WIDTHxHEIGHT in pixels, each side from {SIZE_MIN} to {SIZE_MAX}, as 1500x900")
        elif arg == "--wait":
            wait = parse_wait(value)
            if wait is None:
                raise ShotUsageError(f"--wait is a number of milliseconds from 0 to {WAIT_MAX_MS}")
        elif arg == "--lang":
            lang = value.strip().lower()
            if lang not in {code for code, _label in LANGUAGES}:
                raise ShotUsageError("unknown language code")
        else:
            if not value.strip():
                raise ShotUsageError("--workspace needs a folder")
            workspace = value
    if output is None:
        raise ShotUsageError("--shot needs a file to write")
    return ShotRequest(
        output=Path(output),
        replace=replace,
        size=size if size is not None else DEFAULT_SIZE,
        wait_ms=wait if wait is not None else DEFAULT_WAIT_MS,
        lang=lang,
        workspace=Path(workspace) if workspace is not None else None,
    )


def _missing_value(option: str) -> str:
    return {
        "--shot": "--shot needs a file to write",
        "--size": "--size needs WIDTHxHEIGHT",
        "--wait": "--wait needs a number of milliseconds",
        "--lang": "--lang needs a language code",
        "--workspace": "--workspace needs a folder",
    }[option]


def check_output(request: ShotRequest) -> str | None:
    """Why the picture could not be written to the file asked, or None when it can: the folder is there and an existing file is not replaced without `--replace`."""
    folder = request.output.parent
    if not folder.is_dir():
        return f"the folder of {request.output} does not exist"
    if request.output.is_dir():
        return f"{request.output} is a folder"
    if request.output.exists() and not request.replace:
        return f"{request.output} exists; give --replace to write over it"
    if request.workspace is not None and not request.workspace.is_dir():
        return f"{request.workspace} is not a folder"
    return None
