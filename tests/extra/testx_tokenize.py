# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that need extra dependencies
# Note: Tests requiring TensorFlow/Keras/tltk/torch/transformers have been moved to tests.noauto

import unittest

from pythainlp.tokenize import (
    nercut,
    sent_tokenize,
    ssg,
    subword_tokenize,
    word_tokenize,
)

from ..core.test_tokenize import (
    SENT_1,
    SENT_2,
    SENT_3,
    SENT_4,
    TEXT_1,
)
from ..test_helpers import assert_segment_handles_none_and_empty


class SentTokenizeThaiSumTestCase(unittest.TestCase):
    def test_sent_tokenize_thaisum(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_1,
                engine="thaisum",
            ),
        )
        self.assertIsNotNone(
            sent_tokenize(
                SENT_2,
                engine="thaisum",
            ),
        )
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="thaisum",
            ),
        )
        self.assertEqual(
            sent_tokenize(SENT_4, engine="thaisum"),
            [["ผม", "กิน", "ข้าว", " ", " ", "เธอ", "เล่น", "เกม"]],
        )


class SubwordTokenizeSSGTestCase(unittest.TestCase):
    def test_subword_tokenize_ssg(self):
        assert_segment_handles_none_and_empty(self, ssg.segment)
        self.assertEqual(subword_tokenize(None, engine="ssg"), [])
        self.assertEqual(
            subword_tokenize("แมวกินปลา", engine="ssg"), ["แมว", "กิน", "ปลา"]
        )
        self.assertIn("ดาว", subword_tokenize("สวัสดีดาวอังคาร", engine="ssg"))
        self.assertNotIn("า", subword_tokenize("สวัสดีดาวอังคาร", engine="ssg"))


class WordTokenizeNERCutTestCase(unittest.TestCase):
    def test_word_tokenize_nercut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="nercut"))

    def test_nercut(self):
        assert_segment_handles_none_and_empty(self, nercut.segment)
        self.assertIsNotNone(nercut.segment("ทดสอบ"))
        self.assertEqual(nercut.segment("ทันแน่ๆ"), ["ทัน", "แน่ๆ"])
        self.assertEqual(nercut.segment("%1ครั้ง"), ["%", "1", "ครั้ง"])
        self.assertEqual(nercut.segment("ทุ๊กกโคนน"), ["ทุ๊กกโคนน"])
        self.assertIsNotNone(nercut.segment("อย่าลืมอัพการ์ดนะจ๊ะ"))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="nercut"))


class WordTokenizeBudouxTestCase(unittest.TestCase):
    def test_word_tokenize_budoux(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="budoux"))

