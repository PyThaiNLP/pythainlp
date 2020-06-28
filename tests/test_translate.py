# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import translate


class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.assertIsNotNone(translate("แมวกินปลา", source="th", target="en"))
        self.assertIsNotNone(
            translate(
                "แมวกินปลา",
                source="th",
                target="en",
                tokenizer="word"
            )
        )
        self.assertIsNotNone(
            translate(
                "แมวกินปลา",
                source="th",
                target="en",
                tokenizer="bpe"
            )
        )
        self.assertIsNotNone(
            translate(
                "the cat eats fish.",
                source="en",
                target="th"
            )
        )
        self.assertIsNotNone(
            translate(
                "the cat eats fish.",
                source="en",
                target="th",
                tokenizer="bpe"
            )
        )
