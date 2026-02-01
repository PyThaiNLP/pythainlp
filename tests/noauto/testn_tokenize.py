# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require TensorFlow, Keras, or tltk
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (TensorFlow, Keras)
# - Compilation issues (tltk)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tokenize import (
    attacut,
    deepcut,
    oskut,
    sefr_cut,
    sent_tokenize,
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



class SentTokenizeTLTKTestCaseN(unittest.TestCase):
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



class SubwordTokenizeTLTKTestCaseN(unittest.TestCase):
    def test_subword_tokenize_tltk(self):
        self.assertEqual(subword_tokenize(None, engine="tltk"), [])
        self.assertEqual(subword_tokenize("", engine="tltk"), [])
        self.assertIsInstance(
            subword_tokenize("สวัสดิีดาวอังคาร", engine="tltk"), list
        )
        self.assertNotIn("า", subword_tokenize("สวัสดีดาวอังคาร", engine="tltk"))
        self.assertIsInstance(subword_tokenize("โควิด19", engine="tltk"), list)



class SyllableTokenizeTLTKTestCaseN(unittest.TestCase):
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



class WordTokenizeAttacutTestCaseN(unittest.TestCase):
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



class WordTokenizeDeepcutTestCaseN(unittest.TestCase):
    def test_word_tokenize_deepcut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="deepcut"))

    def test_deepcut(self):
        self.assertEqual(deepcut.segment(None), [])
        self.assertEqual(deepcut.segment(""), [])
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
        self.assertEqual(oskut.segment(None), [])
        self.assertEqual(oskut.segment(""), [])
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
        self.assertEqual(sefr_cut.segment(None), [])
        self.assertEqual(sefr_cut.segment(""), [])
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="tnhc"),
        )



class WordTokenizeTLTKTestCaseN(unittest.TestCase):
    def test_word_tokenize_tltk(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="tltk"))



