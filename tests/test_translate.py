# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import translate

class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.assertIsNone(translate("แมวกินปลา", source="th", target="en"))
        self.assertIsNone(translate("แมวกินปลา", source="th", target="en", tokenizer="word"))
        self.assertIsNone(translate("แมวกินปลา", source="th", target="en", tokenizer="bpe"))
        self.assertIsNone(translate("the cat eat fish.", source="en", target="th"))
        self.assertIsNone(translate("the cat eat fish.", source="en", target="th", tokenizer="bpe"))