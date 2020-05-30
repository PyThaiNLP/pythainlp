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
        self.assertIsNone(__main__.main(["thainlp", "NOT_EXIST", "command"]))

    def test_cli_data(self):
        self.assertIsInstance(getattr(cli, "data"), ModuleType)
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "catalog"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "path"]))
        self.assertIsNotNone(cli.data.App(["thainlp", "data", "info", "test"]))
        self.assertIsNotNone(
            cli.data.App(["thainlp", "data", "get", "NOT_EXIST"])
        )
        self.assertIsNotNone(
            cli.data.App(["thainlp", "data", "rm", "NOT_EXIST"])
        )

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
        self.assertIsInstance(getattr(cli, "data"), ModuleType)
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
