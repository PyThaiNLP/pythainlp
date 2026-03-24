# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.translate import Translate, word_translate
from pythainlp.translate.en_th import (
    EnThTranslator,
    ThEnTranslator,
    download_model_all,
)


class TranslateTestCaseX(unittest.TestCase):
    def test_translate(self):
        # remove("scb_1m_th-en_spm")
        try:
            download_model_all()
        except Exception as e:
            self.fail(f"download_model_all() raised {e}")
        th_en_translator = ThEnTranslator()
        self.assertIsNotNone(
            th_en_translator.translate(
                "แมวกินปลา",
            )
        )
        en_th_translator = EnThTranslator()
        self.assertIsNotNone(
            en_th_translator.translate(
                "the cat eats fish.",
            )
        )
        # Test exclude_words feature
        result_with_exclusion = th_en_translator.translate(
            "แมวกินปลา", exclude_words=["แมว"]
        )
        self.assertIsNotNone(result_with_exclusion)
        self.assertIn("แมว", result_with_exclusion)

        result_with_exclusion_en = en_th_translator.translate(
            "the cat eats fish.", exclude_words=["cat"]
        )
        self.assertIsNotNone(result_with_exclusion_en)
        self.assertIn("cat", result_with_exclusion_en)
        # th_zh_translator = ThZhTranslator()
        # self.assertIsNotNone(
        #     th_zh_translator.translate(
        #         "ผมรักคุณ",
        #     )
        # )
        # zh_th_translator = ZhThTranslator()
        # self.assertIsNotNone(
        #     zh_th_translator.translate(
        #         "我爱你",
        #     )
        # )
        # th_zh_translator = Translate('th', 'zh')
        # self.assertIsNotNone(
        #     th_zh_translator.translate(
        #         "ผมรักคุณ",
        #     )
        # )
        # zh_th_translator = Translate('zh', 'th')
        # self.assertIsNotNone(
        #     zh_th_translator.translate(
        #         "我爱你",
        #     )
        # )
        # th_fr_translator = Translate('th', 'fr')
        # self.assertIsNotNone(
        #     th_fr_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        # th_fr_translator = Translate('th', 'fr', engine="small100")
        # self.assertIsNotNone(
        #     th_fr_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        # th_ja_translator = Translate('th', 'ja', engine="small100")
        # self.assertIsNotNone(
        #     th_ja_translator.translate(
        #         "ทดสอบระบบ",
        #     )
        # )
        with self.assertRaises(ValueError):
            _ = Translate("th", "cat", engine="fkfj")

    def test_word_translate(self):
        self.assertIsNone(word_translate("cat", src="en", target="th"))
        self.assertIsNone(word_translate("แมว", src="en", target="th"))
        self.assertIsNone(
            word_translate("cat", src="en", target="th", engine="word2word")
        )
        self.assertIsNone(
            word_translate("แมว", src="en", target="th", engine="word2word")
        )
        self.assertEqual(
            word_translate("แมว", src="th", target="th", engine="word2word"),
            ["แมว"]
        )

        with self.assertRaises(NotImplementedError):
            word_translate("cat", src="en", target="th", engine="cat")

        with self.assertRaises(NotImplementedError):
            word_translate("แมว", src="th", target="xxx", engine="word2word")
