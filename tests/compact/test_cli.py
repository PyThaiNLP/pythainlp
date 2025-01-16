# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for pythainlp.cli module. (compact)
"""

import unittest

from pythainlp import __main__, cli
from pythainlp.cli.misspell import App as MisspellApp


class CliTestCase(unittest.TestCase):
    def test_cli_misspell(self):
        self.assertTrue(hasattr(cli, "misspell"))

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
                ]
            )
        )
