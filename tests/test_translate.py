# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import translate


class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.assertIsNotNone(
            translate(
                "แมวกินปลา",
                source="th",
                target="en"
            )
        )
        self.assertIsNotNone(
            translate(
                "the cat eats fish.",
                source="en",
                target="th"
            )
        )
