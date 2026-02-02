# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require TensorFlow, Keras, or transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (TensorFlow, Keras, transformers, torch)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tokenize import (
    attacut,
    deepcut,
    oskut,
    paragraph_tokenize,
    sefr_cut,
    sent_tokenize,
    word_dict_trie,
    word_tokenize,
)

from ..core.test_tokenize import (
    SENT_3,
    TEXT_1,
)
from ..test_helpers import (
    assert_segment_handles_none_and_empty,
    assert_subword_tokenize_basic,
)


class DetokenizeTestCaseN(unittest.TestCase):
    def test_numeric_data_format(self):
        engines = ["attacut", "deepcut", "sefr_cut"]

        for engine in engines:
            self.assertIn(
                "127.0.0.1",
                word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine=engine),
            )

            tokens = word_tokenize(
                "เวลา 12:12pm มีโปรโมชั่น 11.11", engine=engine
            )
            self.assertTrue(
                any(value in tokens for value in ["12:12pm", "12:12"]),
                msg=f"{engine}: {tokens}",
            )
            self.assertIn("11.11", tokens)

            self.assertIn(
                "1,234,567.89",
                word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine=engine),
            )

            tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine=engine)
            self.assertIn("2.5:1", tokens)
            self.assertIn("5:2", tokens)

        # try turning off `join_broken_num`
        engine = "attacut"
        self.assertNotIn(
            "127.0.0.1",
            word_tokenize(
                "ไอพีของคุณคือ 127.0.0.1 ครับ",
                engine=engine,
                join_broken_num=False,
            ),
        )
        self.assertNotIn(
            "1,234,567.89",
            word_tokenize(
                "รางวัลมูลค่า 1,234,567.89 บาท",
                engine=engine,
                join_broken_num=False,
            ),
        )


class WordTokenizeAttacutTestCaseN(unittest.TestCase):
    def test_word_tokenize_attacut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="attacut"))

    def test_attacut(self):
        assert_segment_handles_none_and_empty(self, attacut.segment)
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="attacut"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )
        self.assertEqual(
            attacut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", model="attacut-sc"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )
        self.assertIsNotNone(
            attacut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", model="attacut-c")
        )


class WordTokenizeDeepcutTestCaseN(unittest.TestCase):
    def test_word_tokenize_deepcut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="deepcut"))

    def test_deepcut(self):
        assert_segment_handles_none_and_empty(self, deepcut.segment)
        self.assertIsNotNone(deepcut.segment("ทดสอบ", word_dict_trie()))
        self.assertIsNotNone(deepcut.segment("ทดสอบ", ["ทด", "สอบ"]))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="deepcut"))
        self.assertIsNotNone(
            word_tokenize(
                "ทดสอบ", engine="deepcut", custom_dict=word_dict_trie()
            )
        )


class WordTokenizeOSKutTestCaseN(unittest.TestCase):
    def test_word_tokenize_oskut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="oskut"))

    def test_oskut(self):
        assert_segment_handles_none_and_empty(self, oskut.segment)
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="scads"),
        )


class WordTokenizeSEFRCutTestCaseN(unittest.TestCase):
    def test_word_tokenize_sefr_cut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="sefr_cut"))

    def test_sefr_cut(self):
        assert_segment_handles_none_and_empty(self, sefr_cut.segment)
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="tnhc"),
        )


class ParagraphTokenizeTestCaseN(unittest.TestCase):
    def test_paragraph_tokenize(self):
        sent = (
            "(1) บทความนี้ผู้เขียนสังเคราะห์ขึ้นมา"
            "จากผลงานวิจัยที่เคยทำมาในอดีต"
            " มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด"
            " จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ณ ที่นี้"
        )
        self.assertIsNotNone(paragraph_tokenize(sent))
        with self.assertRaises(ValueError):
            paragraph_tokenize(
                sent, engine="ai2+2thai"
            )  # engine does not exist


class SentTokenizeWTPTestCaseN(unittest.TestCase):
    def test_sent_tokenize_wtp(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="wtp",
            ),
        )

    def test_sent_tokenize_wtp_tiny(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="wtp-tiny",
            ),
        )


class SubwordTokenizePhayathaiTestCaseN(unittest.TestCase):
    def test_subword_tokenize_phayathai(self):
        assert_subword_tokenize_basic(self, "phayathai")


class SubwordTokenizeWangchanbertaTestCaseN(unittest.TestCase):
    def test_subword_tokenize_wangchanberta(self):
        assert_subword_tokenize_basic(self, "wangchanberta")
