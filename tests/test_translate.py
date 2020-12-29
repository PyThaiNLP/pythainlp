# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import Translate


class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.translate = Translate()
        self.assertIsNotNone(
            self.translate(
                "แมวกินปลา",
                source="th",
                target="en"
            )
        )
        self.assertIsNotNone(
            self.translate(
                "the cat eats fish.",
                source="en",
                target="th"
            )
        )
