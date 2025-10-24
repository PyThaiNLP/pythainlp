# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that need extra dependencies

import unittest

from pythainlp.tokenize import (
    DEFAULT_WORD_DICT_TRIE,
    attacut,
    deepcut,
    nercut,
    oskut,
    paragraph_tokenize,
    sefr_cut,
    sent_tokenize,
    ssg,
    subword_tokenize,
    tltk,
    word_tokenize,
)

from ..core.test_tokenize import (
    SENT_1,
    SENT_2,
    SENT_3,
    SENT_4,
    TEXT_1,
)


class DetokenizeTestCase(unittest.TestCase):
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


class SentTokenizeTLTKTestCase(unittest.TestCase):
    def test_sent_tokenize_tltk(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_1,
                engine="tltk",
            ),
        )
        self.assertIsNotNone(
            sent_tokenize(
                SENT_2,
                engine="tltk",
            ),
        )
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="tltk",
            ),
        )


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
            [["ผม", "กิน", "ข้าว", " ", "เธอ", "เล่น", "เกม"]],
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


class SubwordTokenizeTLTKTestCase(unittest.TestCase):
    def test_subword_tokenize_tltk(self):
        self.assertEqual(subword_tokenize(None, engine="tltk"), [])
        self.assertEqual(subword_tokenize("", engine="tltk"), [])
        self.assertIsInstance(
            subword_tokenize("สวัสดิีดาวอังคาร", engine="tltk"), list
        )
        self.assertNotIn("า", subword_tokenize("สวัสดีดาวอังคาร", engine="tltk"))
        self.assertIsInstance(subword_tokenize("โควิด19", engine="tltk"), list)


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


class SyllableTokenizeTLTKTestCase(unittest.TestCase):
    def test_tltk(self):
        self.assertEqual(tltk.segment(None), [])
        self.assertEqual(tltk.segment(""), [])
        self.assertEqual(
            tltk.syllable_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
            [
                "ฉัน",
                "รัก",
                "ภา",
                "ษา",
                "ไทย",
                "เพราะ",
                "ฉัน",
                "เป็น",
                "คน",
                "ไทย",
            ],
        )
        self.assertEqual(tltk.syllable_tokenize(None), [])
        self.assertEqual(tltk.syllable_tokenize(""), [])


class WordTokenizeAttacutTestCase(unittest.TestCase):
    def test_word_tokenize_attacut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="attacut"))

    def test_attacut(self):
        self.assertEqual(attacut.segment(None), [])
        self.assertEqual(attacut.segment(""), [])
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


class WordTokenizeDeepcutTestCase(unittest.TestCase):
    def test_word_tokenize_deepcut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="deepcut"))

    def test_deepcut(self):
        self.assertEqual(deepcut.segment(None), [])
        self.assertEqual(deepcut.segment(""), [])
        self.assertIsNotNone(deepcut.segment("ทดสอบ", DEFAULT_WORD_DICT_TRIE))
        self.assertIsNotNone(deepcut.segment("ทดสอบ", ["ทด", "สอบ"]))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="deepcut"))
        self.assertIsNotNone(
            word_tokenize(
                "ทดสอบ", engine="deepcut", custom_dict=DEFAULT_WORD_DICT_TRIE
            )
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


class WordTokenizeOSKutTestCase(unittest.TestCase):
    def test_word_tokenize_oskut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="oskut"))

    def test_oskut(self):
        self.assertEqual(oskut.segment(None), [])
        self.assertEqual(oskut.segment(""), [])
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="scads"),
        )


class WordTokenizeSEFRCutTestCase(unittest.TestCase):
    def test_word_tokenize_sefr_cut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="sefr_cut"))

    def test_sefr_cut(self):
        self.assertEqual(sefr_cut.segment(None), [])
        self.assertEqual(sefr_cut.segment(""), [])
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="tnhc"),
        )


class WordTokenizeTLTKTestCase(unittest.TestCase):
    def test_word_tokenize_tltk(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="tltk"))


class WordTokenizeBudouxTestCase(unittest.TestCase):
    def test_word_tokenize_budoux(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="budoux"))
