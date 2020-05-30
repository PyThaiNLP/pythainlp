# -*- coding: utf-8 -*-

import unittest
from types import ModuleType

from pythainlp import __main__, cli


class TestMainPackage(unittest.TestCase):
    def test_cli_main(self):
        # call with no argument, should exit with 2
        with self.assertRaises(SystemExit) as ex:
            __main__.main()
        self.assertEqual(ex.exception.code, 2)
        self.assertIsNone(__main__.main(["thainlp", "data", "path"]))

    def test_cli_data(self):
        self.assertIsInstance(getattr(cli, "data"), ModuleType)
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "path"]))

    def test_cli_soundex(self):
        self.assertIsInstance(getattr(cli, "soundex"), ModuleType)
        self.assertIsNotNone(cli.soundex.App(["thainlp", "soundex", "ทดสอบ"]))

    def test_cli_tag(self):
        self.assertIsInstance(getattr(cli, "tag"), ModuleType)
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

    def test_cli_tokenize(self):
        self.assertIsInstance(getattr(cli, "data"), ModuleType)
        self.assertIsNotNone(
            cli.tokenize.App(
                [
                    "thainlp",
                    "tokenize",
                    "word",
                    "-a",
                    "newmm",
                    "-s",
                    "|",
                    "ถ้ายิงกระต่ายได้ก็ยิงฟาสซิสต์ได้",
                ]
            )
        )
