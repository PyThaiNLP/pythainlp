# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from argparse import ArgumentError
from types import ModuleType

from pythainlp import __main__, cli


class TestMainPackage(unittest.TestCase):
    def test_cli_main(self):
        # call with no argument, should exit with 2
        with self.assertRaises(SystemExit) as ex:
            __main__.main()
        self.assertEqual(ex.exception.code, 2)

        with self.assertRaises((ArgumentError, SystemExit)):
            self.assertIsNone(__main__.main(["thainlp"]))

        with self.assertRaises((ArgumentError, SystemExit)):
            self.assertIsNone(
                __main__.main(["thainlp", "NOT_EXIST", "command"])
            )

        self.assertIsNone(__main__.main(["thainlp", "data", "path"]))

    def test_cli_benchmark(self):
        self.assertIsInstance(getattr(cli, "benchmark"), ModuleType)

        with self.assertRaises(SystemExit) as ex:
            cli.data.App(["thainlp", "benchmark"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(
            cli.benchmark.App(
                [
                    "thainlp",
                    "benchmark",
                    "word-tokenization",
                    "--input-file",
                    "./tests/data/input.txt",
                    "--test-file",
                    "./tests/data/test.txt",
                    "--save-details",
                ]
            )
        )

    def test_cli_data(self):
        self.assertIsInstance(getattr(cli, "data"), ModuleType)

        with self.assertRaises(SystemExit) as ex:
            cli.data.App(["thainlp", "data"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(cli.data.App(["thainlp", "data", "catalog"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "path"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "get", "test"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "info", "test"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "rm", "test"]))
        self.assertIsNotNone(
            cli.data.App(["thainlp", "data", "get", "NOT_EXIST"])
        )
        self.assertIsNotNone(
            cli.data.App(["thainlp", "data", "info", "NOT_EXIST"])
        )
        self.assertIsNotNone(
            cli.data.App(["thainlp", "data", "rm", "NOT_EXIST"])
        )

    def test_cli_soundex(self):
        self.assertIsInstance(getattr(cli, "soundex"), ModuleType)

        with self.assertRaises(SystemExit) as ex:
            cli.data.App(["thainlp", "soundex"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(cli.soundex.App(["thainlp", "soundex", "ทดสอบ"]))

    def test_cli_tag(self):
        self.assertIsInstance(getattr(cli, "tag"), ModuleType)

        with self.assertRaises(SystemExit) as ex:
            cli.data.App(["thainlp", "tag"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(
            cli.tag.App(
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
            cli.tag.App(
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
        self.assertIsInstance(getattr(cli, "tokenize"), ModuleType)

        with self.assertRaises(SystemExit) as ex:
            cli.data.App(["thainlp", "tokenize"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(
            cli.tokenize.App(["thainlp", "tokenize", "NOT_EXIST", "ไม่มีอยู่ จริง"])
        )
        self.assertIsNotNone(
            cli.tokenize.App(
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
            cli.tokenize.App(
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
            cli.tokenize.App(
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
        self.assertIsNotNone(
            cli.tokenize.App(
                [
                    "thainlp",
                    "tokenize",
                    "sent",
                    "-s",
                    "|",
                    (
                        "ถ้าฉันยิงกระต่ายได้ ฉันก็ยิงฟาสซิสต์ได้"
                        "กระสุนสำหรับสมองของคุณวันนี้"
                        "แต่คุณก็จะลืมมันไปทั้งหมดอีกครั้ง"
                    ),
                ]
            )
        )
