# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from argparse import ArgumentError

from pythainlp import __main__, cli
from pythainlp.cli.data import App as DataApp
from pythainlp.cli.soundex import App as SoundexApp
from pythainlp.cli.tag import App as TagApp
from pythainlp.cli.tokenize import App as TokenizeApp


class CliTestCase(unittest.TestCase):
    def test_cli(self):
        with self.assertRaises((ArgumentError, SystemExit)):
            cli.exit_if_empty("", None)

    def test_cli_main(self):
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

        with self.assertRaises(SystemExit) as ex:
            DataApp(["thainlp", "data"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(DataApp(["thainlp", "data", "catalog"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "path"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "get", "test"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "info", "test"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "rm", "test"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "get", "NOT_EXIST"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "info", "NOT_EXIST"]))
        self.assertIsNotNone(DataApp(["thainlp", "data", "rm", "NOT_EXIST"]))

    def test_cli_soundex(self):
        self.assertTrue(hasattr(cli, "soundex"))

        with self.assertRaises(SystemExit) as ex:
            DataApp(["thainlp", "soundex"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(SoundexApp(["thainlp", "soundex", "ทดสอบ"]))

    def test_cli_tag(self):
        self.assertTrue(hasattr(cli, "tag"))

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
