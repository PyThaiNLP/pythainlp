# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require torch and transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers, attacut)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tokenize import (
    attacut,
    paragraph_tokenize,
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


class DetokenizeAttacutTestCaseN(unittest.TestCase):
    """Tests for attacut tokenizer numeric handling (requires torch)"""

    def test_numeric_data_format_attacut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="attacut"),
        )

        tokens = word_tokenize(
            "เวลา 12:12pm มีโปรโมชั่น 11.11", engine="attacut"
        )
        self.assertTrue(
            any(value in tokens for value in ["12:12pm", "12:12"]),
            msg=f"attacut: {tokens}",
        )
        self.assertIn("11.11", tokens)

        self.assertIn(
            "1,234,567.89",
            word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine="attacut"),
        )

        tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine="attacut")
        self.assertIn("2.5:1", tokens)
        self.assertIn("5:2", tokens)

        # try turning off `join_broken_num`
        self.assertNotIn(
            "127.0.0.1",
            word_tokenize(
                "ไอพีของคุณคือ 127.0.0.1 ครับ",
                engine="attacut",
                join_broken_num=False,
            ),
        )
        self.assertNotIn(
            "1,234,567.89",
            word_tokenize(
                "รางวัลมูลค่า 1,234,567.89 บาท",
                engine="attacut",
                join_broken_num=False,
            ),
        )


class WordTokenizeAttacutTestCaseN(unittest.TestCase):
    """Tests for attacut tokenizer (requires torch)"""

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


class ParagraphTokenizeTestCaseN(unittest.TestCase):
    """Tests for paragraph tokenization (requires transformers)"""

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
    """Tests for WTP sentence tokenizer (requires transformers and torch)"""

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
    """Tests for phayathai subword tokenizer (requires transformers)"""

    def test_subword_tokenize_phayathai(self):
        assert_subword_tokenize_basic(self, "phayathai")


class SubwordTokenizeWangchanbertaTestCaseN(unittest.TestCase):
    """Tests for wangchanberta subword tokenizer (requires transformers)"""

    def test_subword_tokenize_wangchanberta(self):
        assert_subword_tokenize_basic(self, "wangchanberta")
