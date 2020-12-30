# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import EnThTranslator, ThEnTranslator


class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.th_en_translator = ThEnTranslator()
        self.assertIsNotNone(
            self.th_en_translator.translate(
                "แมวกินปลา",
            )
        )
        self.en_th_translator = EnThTranslator()
        self.assertIsNotNone(
            self.en_th_translator.translate(
                "the cat eats fish.",
            )
        )
