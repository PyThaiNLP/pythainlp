# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import io
import unittest
from argparse import ArgumentError
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import MagicMock, patch

from pythainlp import __main__, cli
from pythainlp.cli.data import App as DataApp
from pythainlp.cli.misspell import App as MisspellApp
from pythainlp.cli.soundex import App as SoundexApp
from pythainlp.cli.tag import App as TagApp
from pythainlp.cli.tokenize import App as TokenizeApp


class CliTestCase(unittest.TestCase):
    def test_cli(self):
        with self.assertRaises((ArgumentError, SystemExit)):
            cli.exit_if_empty("", None)

    def test_cli_main(self):
        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            # call with no argument, should exit with 2
            with self.assertRaises(SystemExit) as ex:
                __main__.main()
            self.assertEqual(ex.exception.code, 2)

            with self.assertRaises((ArgumentError, SystemExit)):
                __main__.main(["thainlp"])

            with self.assertRaises((ArgumentError, SystemExit)):
                __main__.main(["thainlp", "NOT_EXIST", "command"])

            self.assertIsNone(__main__.main(["thainlp", "data", "path"]))

    def test_cli_data(self):
        self.assertTrue(hasattr(cli, "data"))

        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                DataApp(["thainlp", "data"])
            self.assertEqual(ex.exception.code, 2)

            # Mock network calls to avoid corpus downloads
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "test": {"latest_version": "0.1", "versions": {}},
            }

            with patch("pythainlp.corpus.get_corpus_db", return_value=mock_response):
                self.assertIsNotNone(DataApp(["thainlp", "data", "catalog"]))

            self.assertIsNotNone(DataApp(["thainlp", "data", "path"]))

            # Mock download to avoid network
            with patch("pythainlp.corpus.download", return_value=True):
                self.assertIsNotNone(DataApp(["thainlp", "data", "get", "test"]))

            self.assertIsNotNone(DataApp(["thainlp", "data", "info", "test"]))

            # Mock remove to avoid side effects
            with patch("pythainlp.corpus.remove", return_value=True):
                self.assertIsNotNone(DataApp(["thainlp", "data", "rm", "test"]))

            # Test with non-existing corpus
            with patch("pythainlp.corpus.download", return_value=False):
                self.assertIsNotNone(DataApp(["thainlp", "data", "get", "NOT_EXIST"]))

            self.assertIsNotNone(DataApp(["thainlp", "data", "info", "NOT_EXIST"]))

            with patch("pythainlp.corpus.remove", return_value=False):
                self.assertIsNotNone(DataApp(["thainlp", "data", "rm", "NOT_EXIST"]))

    def test_cli_misspell(self):
        self.assertTrue(hasattr(cli, "misspell"))

        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                MisspellApp(["thainlp", "misspell"])
            self.assertEqual(ex.exception.code, 2)

            self.assertIsNotNone(
                MisspellApp(
                    [
                        "thainlp",
                        "misspell",
                        "--file",
                        "./tests/data/text.txt",
                        "--seed",
                        "1",
                        "--misspell-ratio",
                        "0.05",
                        "--output",
                        "./tests/data/misspell_output.tmp",
                    ]
                )
            )

    def test_cli_soundex(self):
        self.assertTrue(hasattr(cli, "soundex"))

        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                DataApp(["thainlp", "soundex"])
            self.assertEqual(ex.exception.code, 2)

            self.assertIsNotNone(SoundexApp(["thainlp", "soundex", "ทดสอบ"]))

    def test_cli_tag(self):
        self.assertTrue(hasattr(cli, "tag"))

        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                DataApp(["thainlp", "tag"])
            self.assertEqual(ex.exception.code, 2)

            self.assertIsNotNone(
                TagApp(
                    [
                        "thainlp",
                        "tag",
                        "pos",
                        "-s",
                        " ",
                        "มอเตอร์ไซค์ ความว่างเปล่า",
                    ]
                )
            )
            self.assertIsNotNone(
                TagApp(
                    [
                        "thainlp",
                        "tag",
                        "role",
                        "-s",
                        " ",
                        "มอเตอร์ไซค์ ความว่างเปล่า",
                    ]
                )
            )

    def test_cli_tokenize(self):
        self.assertTrue(hasattr(cli, "tokenize"))

        # Suppress output to keep test log clean
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                DataApp(["thainlp", "tokenize"])
            self.assertEqual(ex.exception.code, 2)

            self.assertIsNotNone(
                TokenizeApp(["thainlp", "tokenize", "NOT_EXIST", "ไม่มีอยู่ จริง"])
            )
            self.assertIsNotNone(
                TokenizeApp(
                    [
                        "thainlp",
                        "tokenize",
                        "subword",
                        "-s",
                        "|",
                        "ถ้าฉันยิงกระต่ายได้ ฉันก็ยิงฟาสซิสต์ได้",
                    ]
                )
            )
            self.assertIsNotNone(
                TokenizeApp(
                    [
                        "thainlp",
                        "tokenize",
                        "syllable",
                        "-s",
                        "|",
                        "-w",
                        "ถ้าฉันยิงกระต่ายได้ ฉันก็ยิงฟาสซิสต์ได้",
                    ]
                )
            )
            self.assertIsNotNone(
                TokenizeApp(
                    [
                        "thainlp",
                        "tokenize",
                        "word",
                        "-nw",
                        "-a",
                        "newmm",
                        "-s",
                        "|",
                        "ถ้าฉันยิงกระต่ายได้ ฉันก็ยิงฟาสซิสต์ได้",
                    ]
                )
            )
