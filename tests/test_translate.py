# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import (
    EnThTranslator,
    ThEnTranslator,
    ThZhTranslator,
    ZhThTranslator,
    download_model_all
)


class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        self.assertIsNone(download_model_all())
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
        self.th_zh_translator = ThZhTranslator()
        self.assertIsNotNone(
            self.th_zh_translator.translate(
                "ผมรักคุณ",
            )
        )
        self.zh_th_translator = ZhThTranslator()
        self.assertIsNotNone(
            self.zh_th_translator.translate(
                "我爱你",
            )
        )
