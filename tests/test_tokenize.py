# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.corpus.common import _THAI_WORDS_FILENAME
from pythainlp.corpus import (
    _CORPUS_PATH,
    thai_words,
)
from pythainlp.tokenize import DEFAULT_DICT_TRIE, Tokenizer
from pythainlp.tokenize import deepcut as tokenize_deepcut
from pythainlp.tokenize import attacut
from pythainlp.tokenize import (
    dict_trie,
    dict_word_tokenize,
    etcc,
    longest,
    multi_cut,
    newmm,
)
from pythainlp.tokenize import pyicu as tokenize_pyicu
from pythainlp.tokenize import (
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    tcc,
    word_tokenize,
)


class TestTokenizePackage(unittest.TestCase):

    def test_dict_word_tokenize(self):
        self.assertEqual(dict_word_tokenize(""), [])

    def test_etcc(self):
        self.assertEqual(etcc.segment(""), "")
        self.assertIsInstance(etcc.segment("คืนความสุข"), list)
        self.assertIsNotNone(
            etcc.segment(
                "หมูแมวเหล่านี้ด้วยเหตุผลเชื่อมโยงทางกรรมพันธุ์" +
                "สัตว์มีแขนขาหน้าหัวเราะเพราะแข็งขืน"
            )
        )

    def test_word_tokenize(self):
        self.assertEqual(word_tokenize(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="newmm")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="mm")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="longest")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="icu")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="deepcut")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="XX")
        )
        self.assertIsNotNone(
            word_tokenize("หมอนทองตากลมหูว์MBK39", engine="attacut")
        )

        self.assertIsNotNone(dict_trie(()))
        self.assertIsNotNone(dict_trie(("ทดสอบ", "สร้าง", "Trie")))
        self.assertIsNotNone(dict_trie(["ทดสอบ", "สร้าง", "Trie"]))
        self.assertIsNotNone(dict_trie(thai_words()))
        self.assertIsNotNone(dict_trie(DEFAULT_DICT_TRIE))
        self.assertIsNotNone(
            dict_trie(os.path.join(_CORPUS_PATH, _THAI_WORDS_FILENAME))
        )

        self.assertIsNotNone(
            word_tokenize("รถไฟฟ้าBTS", custom_dict=DEFAULT_DICT_TRIE)
        )

    def test_Tokenizer(self):
        t_test = Tokenizer(DEFAULT_DICT_TRIE)
        self.assertEqual(t_test.word_tokenize(""), [])
        t_test.set_tokenize_engine("longest")
        self.assertEqual(t_test.word_tokenize(None), [])

        t_test = Tokenizer()
        self.assertEqual(t_test.word_tokenize("ก"), ["ก"])

    def test_word_tokenize_icu(self):
        self.assertEqual(tokenize_pyicu.segment(None), [])
        self.assertEqual(tokenize_pyicu.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="icu"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_word_tokenize_deepcut(self):
        self.assertEqual(tokenize_deepcut.segment(None), [])
        self.assertEqual(tokenize_deepcut.segment(""), [])
        self.assertIsNotNone(
            tokenize_deepcut.segment("ทดสอบ", DEFAULT_DICT_TRIE)
        )
        self.assertIsNotNone(tokenize_deepcut.segment("ทดสอบ", ["ทด", "สอบ"]))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="deepcut"))
        self.assertIsNotNone(
            word_tokenize(
                "ทดสอบ",
                engine="deepcut",
                custom_dict=DEFAULT_DICT_TRIE
            )
        )

    def test_word_tokenize_longest(self):
        self.assertEqual(longest.segment(None), [])
        self.assertEqual(longest.segment(""), [])
        self.assertIsNotNone(longest.segment("กรุงเทพฯมากๆเพราโพาง BKKฯ"))
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="longest"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

    def test_word_tokenize_mm(self):
        self.assertEqual(multi_cut.segment(None), [])
        self.assertEqual(multi_cut.segment(""), [])
        self.assertEqual(word_tokenize("", engine="mm"), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="mm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

        self.assertIsNotNone(multi_cut.mmcut("ทดสอบ"))

        self.assertIsNotNone(
            multi_cut.find_all_segment("รถไฟฟ้ากรุงเทพมหานครBTS")
        )
        self.assertEqual(multi_cut.find_all_segment(None), [])

    def test_word_tokenize_newmm(self):
        self.assertEqual(newmm.segment(None), [])
        self.assertEqual(newmm.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="newmm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )
        self.assertEqual(
            word_tokenize(
                "สวัสดีครับ สบายดีไหมครับ",
                engine="newmm",
                keep_whitespace=True
            ),
            ["สวัสดี", "ครับ", " ", "สบายดี", "ไหม", "ครับ"],
        )
        self.assertEqual(
            word_tokenize("จุ๋มง่วงนอนยัง", engine="newmm"),
            ["จุ๋ม", "ง่วงนอน", "ยัง"]
        )
        self.assertEqual(
            word_tokenize("จุ๋มง่วง", engine="newmm"),
            ["จุ๋ม", "ง่วง"]
        )
        self.assertEqual(
            word_tokenize(
                "จุ๋ม   ง่วง",
                engine="newmm",
                keep_whitespace=False
            ),
            ["จุ๋ม", "ง่วง"],
        )


    def test_word_tokenize_attacut(self):
        self.assertEqual(attacut.segment(None), [])
        self.assertEqual(attacut.segment(""), [])
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="attacut"),
            ['ฉัน', 'รัก', 'ภาษา', 'ไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คน', 'ไทย'],
        )


    def test_sent_tokenize(self):
        self.assertEqual(sent_tokenize(None), [])
        self.assertEqual(sent_tokenize(""), [])
        self.assertEqual(
            sent_tokenize("รักน้ำ  รักปลา  ", engine="whitespace"),
            ["รักน้ำ", "รักปลา", ""],
        )
        self.assertEqual(
            sent_tokenize("รักน้ำ  รักปลา  "),
            ["รักน้ำ", "รักปลา"]
        )

    def test_subword_tokenize(self):
        self.assertEqual(subword_tokenize(None), [])
        self.assertEqual(subword_tokenize(""), [])
        self.assertIsNotNone(
            subword_tokenize("สวัสดีดาวอังคาร", engine="tcc"))
        self.assertIsNotNone(
            subword_tokenize("สวัสดีดาวอังคาร", engine="etcc")
        )

    def test_syllable_tokenize(self):
        self.assertEqual(syllable_tokenize(None), [])
        self.assertEqual(syllable_tokenize(""), [])
        self.assertEqual(
            syllable_tokenize("สวัสดีชาวโลก"),
            ["สวัส", "ดี", "ชาว", "โลก"]
        )
        self.assertEqual(
            syllable_tokenize("แมวกินปลา", engine="ssg"),
            ['แมว', 'กิน', 'ปลา']
        )

    def test_tcc(self):
        self.assertEqual(tcc.segment(None), [])
        self.assertEqual(tcc.segment(""), [])
        self.assertEqual(
            tcc.segment("ประเทศไทย"),
            ["ป", "ระ", "เท", "ศ", "ไท", "ย"]
        )

        self.assertEqual(list(tcc.tcc("")), [])
        self.assertEqual(tcc.tcc_pos(""), set())
