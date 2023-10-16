# -*- coding: utf-8 -*-

import unittest

from pythainlp.translate import Translate
from pythainlp.translate.en_th import (
    EnThTranslator,
    ThEnTranslator,
    download_model_all
)

class TestTranslatePackage(unittest.TestCase):
    def test_translate(self):
        # remove("scb_1m_th-en_spm")
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
        # self.th_zh_translator = ThZhTranslator()
        # self.assertIsNotNone(
        #     self.th_zh_translator.translate(
        #         "ผมรักคุณ",
        #     )
        # )
        # self.zh_th_translator = ZhThTranslator()
        # self.assertIsNotNone(
        #     self.zh_th_translator.translate(
        #         "我爱你",
        #     )
        # )
        # self.th_zh_translator = Translate('th', 'zh')
        # self.assertIsNotNone(
        #     self.th_zh_translator.translate(
        #         "ผมรักคุณ",
        #     )
        # )
        # self.zh_th_translator = Translate('zh', 'th')
        # self.assertIsNotNone(
        #     self.zh_th_translator.translate(
        #         "我爱你",
        #     )
        # )
        # self.th_fr_translator = Translate('th', 'fr')
        # self.assertIsNotNone(
        #     self.th_fr_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        # self.th_fr_translator = Translate('th', 'fr', engine="small100")
        # self.assertIsNotNone(
        #     self.th_fr_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        # self.th_ja_translator = Translate('th', 'ja', engine="small100")
        # self.assertIsNotNone(
        #     self.th_fr_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        with self.assertRaises(ValueError):
            self.th_cat_translator = Translate('th', 'cat', engine="fkfj")
