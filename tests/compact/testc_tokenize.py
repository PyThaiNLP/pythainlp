# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that need "compact" dependencies

import unittest

from pythainlp.tokenize import (
    pyicu,
    sent_tokenize,
    subword_tokenize,
    word_tokenize,
)

from ..core.test_tokenize import (
    SENT_1,
    SENT_1_TOKS,
    SENT_2,
    SENT_2_TOKS,
    SENT_3,
    SENT_3_TOKS,
    SENT_4,
    TEXT_1,
)
from ..test_helpers import assert_segment_handles_none_and_empty


class SentTokenizeCRFCutTestCaseC(unittest.TestCase):
    def test_sent_tokenize(self):
        # Use default engine (crfcut)
        self.assertEqual(sent_tokenize(None), [])
        self.assertEqual(sent_tokenize(""), [])
        self.assertEqual(
            sent_tokenize(SENT_1),
            SENT_1_TOKS,
        )
        self.assertEqual(
            sent_tokenize(SENT_2),
            SENT_2_TOKS,
        )
        self.assertEqual(
            sent_tokenize(SENT_3),
            SENT_3_TOKS,
        )

        self.assertEqual(
            sent_tokenize(SENT_1, engine="crfcut"),
            SENT_1_TOKS,
        )
        self.assertEqual(
            sent_tokenize(SENT_2, engine="crfcut"),
            SENT_2_TOKS,
        )
        self.assertEqual(
            sent_tokenize(SENT_3, engine="crfcut"),
            SENT_3_TOKS,
        )
        self.assertEqual(
            sent_tokenize(SENT_4, engine="crfcut"),
            [["ผม", "กิน", "ข้าว", " ", "\n", "เธอ", "เล่น", "เกม"]],
        )


class SubwordTokenizeHanSoloTestCaseC(unittest.TestCase):
    def test_subword_tokenize(self):
        self.assertEqual(subword_tokenize(None, engine="han_solo"), [])
        self.assertEqual(
            subword_tokenize("แมวกินปลา", engine="han_solo"),
            ["แมว", "กิน", "ปลา"],
        )
        self.assertIn(
            "ดาว", subword_tokenize("สวัสดีดาวอังคาร", engine="han_solo")
        )

        self.assertNotIn(
            "า", subword_tokenize("สวัสดีดาวอังคาร", engine="han_solo")
        )


class WordTokenizeICUTestCaseC(unittest.TestCase):
    def test_icu(self):
        assert_segment_handles_none_and_empty(self, pyicu.segment)
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="icu"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_word_tokenize_icu(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="icu"))


class WordTokenizeNlpO3TestCaseC(unittest.TestCase):
    def test_word_tokenize_nlpo3(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="nlpo3"))
        self.assertEqual(word_tokenize("การ์", engine="nlpo3"), ["การ์"])
