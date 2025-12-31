# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp import __main__, cli
from pythainlp.cli.benchmark import App as BenchmarkApp
from pythainlp.cli.data import App as DataApp
from pythainlp.cli.tokenize import App as TokenizeApp


class CliTestCaseX(unittest.TestCase):
    def test_cli_benchmark(self):
        self.assertTrue(hasattr(cli, "benchmark"))

        with self.assertRaises(SystemExit) as ex:
            DataApp(["thainlp", "benchmark"])
        self.assertEqual(ex.exception.code, 2)

        self.assertIsNotNone(
            BenchmarkApp(
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

    def test_cli_tokenize(self):
        self.assertIsNotNone(
            TokenizeApp(
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
