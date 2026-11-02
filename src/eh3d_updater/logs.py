# =============================================================================
# EH3D-UPDATER - Log file rotation: logs.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Keeps the folder of window log files from growing without limit.

The window writes one log file per run. This keeps the newest ones and
removes the rest; a file that cannot be removed is simply left."""
from __future__ import annotations

import contextlib
import logging
import os
import sys
import time
from pathlib import Path
from typing import Iterator

#: Pattern of the log files the command line writes (the window writes ``gui_*.log`` in the same folder).
CLI_LOG_PATTERN = "cli_*.log"
#: Environment variable that moves the folder of the log files (tests and scheduled tasks use it).
LOG_DIR_ENV = "EH3D_UPDATER_LOG_DIR"

#: How many window log files are kept.
DEFAULT_LOGS_TO_KEEP = 20


def prune_logs(directory: Path, keep: int = DEFAULT_LOGS_TO_KEEP, pattern: str = "gui_*.log") -> list[Path]:
    """Removes the oldest files matching `pattern` in `directory` beyond the
    newest `keep`. Returns the files removed."""
    try:
        files = sorted(
            (path for path in directory.glob(pattern) if path.is_file()),
            key=lambda path: (path.stat().st_mtime, path.name),
            reverse=True,
        )
    except OSError:
        return []
    removed: list[Path] = []
    for path in files[max(keep, 0):]:
        try:
            path.unlink()
        except OSError:
            continue
        removed.append(path)
    return removed


def default_log_dir() -> Path:
    """The folder of the log files: ``EH3D_UPDATER_LOG_DIR`` when set, otherwise the one of the window."""
    override = os.environ.get(LOG_DIR_ENV, "").strip()
    return Path(override) if override else Path.home() / ".eh3d_updater" / "logs"


class _Tee:
    """Writes to the real stream and, line by line, to the log. Everything else is the real stream's."""

    def __init__(self, stream, logger: logging.Logger, level: int) -> None:
        self._stream, self._logger, self._level, self._pending = stream, logger, level, ""

    def write(self, data: str) -> int:
        written = self._stream.write(data)
        self._pending += data
        while "\n" in self._pending:
            line, self._pending = self._pending.split("\n", 1)
            if line.strip():
                self._logger.log(self._level, line.rstrip("\r"))
        return written

    def flush(self) -> None:
        self._stream.flush()

    def finish(self) -> None:
        if self._pending.strip():
            self._logger.log(self._level, self._pending.rstrip())
        self._pending = ""

    def __getattr__(self, name: str):
        return getattr(self._stream, name)


@contextlib.contextmanager
def cli_log(argv: list[str], *, version: str, file: Path | None = None, directory: Path | None = None, keep: int = DEFAULT_LOGS_TO_KEEP) -> Iterator[Path | None]:
    """Records a command-line run in a log file: the command, every line it prints (standard output and error) and how it ended.

    `file` names the log exactly; otherwise a new ``cli_<time>.log`` is made in `directory`
    (default: `default_log_dir()`) and the oldest ones beyond `keep` are removed. A log that cannot be
    written is skipped (the command still runs); the path, or None, is what the block receives."""
    if file is not None:
        path = file
    else:
        path = (directory or default_log_dir()) / f"cli_{time.strftime('%Y%m%d_%H%M%S')}_{os.getpid()}.log"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(path, encoding="utf-8")
    except OSError:
        yield None
        return
    logger = logging.getLogger(f"eh3d_updater.cli.{id(handler)}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    out, err = _Tee(sys.stdout, logger, logging.INFO), _Tee(sys.stderr, logger, logging.WARNING)
    real_out, real_err = sys.stdout, sys.stderr
    logger.info("EH3D Updater %s command line: %s", version, " ".join(argv))
    sys.stdout, sys.stderr = out, err
    try:
        yield path
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            logger.info("exit %s", exc.code)
        else:
            import traceback
            logger.error("UNHANDLED EXCEPTION:\n%s", "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        raise
    finally:
        out.finish()
        err.finish()
        sys.stdout, sys.stderr = real_out, real_err
        logger.removeHandler(handler)
        handler.close()
        if file is None:
            prune_logs(path.parent, keep, CLI_LOG_PATTERN)


def log_result(path: Path | None, code: int) -> None:
    """Appends the exit code of a finished run to its log."""
    if path is None:
        return
    try:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} INFO exit code {code}\n")
    except OSError:
        pass


def announce_log(path: Path | None, *, failed: bool) -> None:
    """After a failed run, tells where its log is (on the error stream, after the log was closed, so the line is not inside the log itself)."""
    if failed and path is not None:
        print(f"Full log: {path}", file=sys.stderr)
