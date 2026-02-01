# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that need extra dependencies
# Note: Tests requiring TensorFlow/Keras/tltk have been moved to tests.noautotest

import unittest

from pythainlp.tokenize import (
    nercut,
    paragraph_tokenize,
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


class ParagraphTokenizeTestCase(unittest.TestCase):
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


class SentTokenizeWTPTestCase(unittest.TestCase):
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
        # self.assertIsNotNone(
        #     sent_tokenize(
        #         SENT_3,
        #         engine="wtp-base",
        #     ),
        # )
        # self.assertIsNotNone(
        #     sent_tokenize(
        #         SENT_3,
        #         engine="wtp-large",
        #     ),
        # )


class SubwordTokenizePhayathaiTestCase(unittest.TestCase):
    def test_subword_tokenize_phayathai(self):
        self.assertEqual(subword_tokenize(None, engine="phayathai"), [])
        self.assertEqual(subword_tokenize("", engine="phayathai"), [])
        self.assertIsInstance(
            subword_tokenize("สวัสดิีดาวอังคาร", engine="phayathai"), list
        )
        self.assertNotIn(
            "า", subword_tokenize("สวัสดีดาวอังคาร", engine="phayathai")
        )
        self.assertIsInstance(
            subword_tokenize("โควิด19", engine="phayathai"), list
        )


class SubwordTokenizeSSGTestCase(unittest.TestCase):
    def test_subword_tokenize_ssg(self):
        self.assertEqual(ssg.segment(None), [])
        self.assertEqual(ssg.segment(""), [])
        self.assertEqual(subword_tokenize(None, engine="ssg"), [])
        self.assertEqual(
            subword_tokenize("แมวกินปลา", engine="ssg"), ["แมว", "กิน", "ปลา"]
        )
        self.assertIn("ดาว", subword_tokenize("สวัสดีดาวอังคาร", engine="ssg"))
        self.assertNotIn("า", subword_tokenize("สวัสดีดาวอังคาร", engine="ssg"))


class SubwordTokenizeWangchanbertaTestCase(unittest.TestCase):
    def test_subword_tokenize_wangchanberta(self):
        self.assertEqual(subword_tokenize(None, engine="wangchanberta"), [])
        self.assertEqual(subword_tokenize("", engine="wangchanberta"), [])
        self.assertIsInstance(
            subword_tokenize("สวัสดิีดาวอังคาร", engine="wangchanberta"), list
        )
        self.assertNotIn(
            "า", subword_tokenize("สวัสดีดาวอังคาร", engine="wangchanberta")
        )
        self.assertIsInstance(
            subword_tokenize("โควิด19", engine="wangchanberta"), list
        )


class WordTokenizeNERCutTestCase(unittest.TestCase):
    def test_word_tokenize_nercut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="nercut"))

    def test_nercut(self):
        self.assertEqual(nercut.segment(None), [])
        self.assertEqual(nercut.segment(""), [])
        self.assertIsNotNone(nercut.segment("ทดสอบ"))
        self.assertEqual(nercut.segment("ทันแน่ๆ"), ["ทัน", "แน่ๆ"])
        self.assertEqual(nercut.segment("%1ครั้ง"), ["%", "1", "ครั้ง"])
        self.assertEqual(nercut.segment("ทุ๊กกโคนน"), ["ทุ๊กกโคนน"])
        self.assertIsNotNone(nercut.segment("อย่าลืมอัพการ์ดนะจ๊ะ"))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="nercut"))


class WordTokenizeBudouxTestCase(unittest.TestCase):
    def test_word_tokenize_budoux(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="budoux"))

