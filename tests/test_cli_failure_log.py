# =============================================================================
# EH3D-UPDATER - tests/test_cli_failure_log.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A command that fails tells where its log is, also when it ends with an unexpected error."""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from eh3d_updater import logs
from eh3d_updater import main as main_module


class FailureLogTests(unittest.TestCase):
    def run_main(self, argv: list[str], func) -> tuple:
        err = io.StringIO()
        error = None
        code = None
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {logs.LOG_DIR_ENV: tmp}):
            parser = main_module.build_parser()
            args = parser.parse_args(argv)
            args.func = func
            with mock.patch.object(sys, "argv", ["eh3d-updater", "--cli", *argv]), mock.patch.object(main_module, "build_parser") as build:
                build.return_value.parse_args.return_value = args
                with contextlib.redirect_stderr(err):
                    try:
                        code = main_module.main()
                    except Exception as exc:  # noqa: BLE001 - the test looks at what comes out
                        error = exc
            written = sorted(Path(tmp).glob("cli_*.log"))
            return code, err.getvalue(), (written[0] if written else Path()), error, written[0].read_text(encoding="utf-8") if written else ""

    def test_a_failed_command_says_where_the_full_log_is(self) -> None:
        code, err, log, error, text = self.run_main(["status", "--offline"], lambda a: 1)
        self.assertEqual(code, 1)
        self.assertIn("Full log: ", err)
        self.assertIn(log.name, err)
        self.assertIn("exit code 1", text)

    def test_a_clean_run_and_the_updates_available_code_do_not_ask_to_read_the_log(self) -> None:
        for wanted in (0, main_module.EXIT_UPDATES_AVAILABLE):
            code, err, _, _, _ = self.run_main(["status", "--offline"], lambda a, w=wanted: w)
            self.assertEqual(code, wanted)
            self.assertNotIn("Full log", err)

    def test_an_unexpected_error_leaves_the_traceback_in_the_log_and_names_it(self) -> None:
        def broken(args):
            raise RuntimeError("the disk went away")

        code, err, _, error, text = self.run_main(["status", "--offline"], broken)
        self.assertIsNone(code)
        self.assertIsInstance(error, RuntimeError)
        self.assertIn("Full log: ", err)
        self.assertIn("UNHANDLED EXCEPTION", text)
        self.assertIn("the disk went away", text)

    def test_announce_log_is_silent_without_a_log_or_without_failure(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            logs.announce_log(None, failed=True)
            logs.announce_log(Path("x.log"), failed=False)
        self.assertEqual(err.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
