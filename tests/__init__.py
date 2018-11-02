# -*- coding: utf-8 -*-
import sys
import unittest
from collections import Counter

from pythainlp.change import texttoeng, texttothai
from pythainlp.collation import collate
from pythainlp.corpus import (
    countries,
    provinces,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
    ttc,
    wordnet,
)
from pythainlp.corpus.conceptnet import edges
from pythainlp.corpus.tnc import get_word_frequency_all
from pythainlp.date import now, now_reign_year, reign_year_to_ad
from pythainlp.g2p import ipa
from pythainlp.keywords import find_keyword
from pythainlp.ner import ThaiNameRecognizer
from pythainlp.number import numtowords
from pythainlp.rank import rank
from pythainlp.romanization import romanize
from pythainlp.soundex import lk82, metasound, udom83
from pythainlp.spell import spell, correct
from pythainlp.summarize import summarize
from pythainlp.tag import pos_tag, pos_tag_sents
from pythainlp.tokenize import etcc, isthai, syllable_tokenize, tcc, word_tokenize
from pythainlp.util import listtext_num2num, normalize


class TestUM(unittest.TestCase):
    """
    ทดสอบการทำงาน
    """

    def test_segment(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

    def test_syllable_tokenize(self):
        self.assertEqual(
            syllable_tokenize("สวัสดีชาวโลก"), ["สวัส", "ดี", "ชาว", "โลก"]
        )

    def test_segment_icu(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="icu"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_segment_mm(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="mm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

    def test_segment_newmm(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="newmm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )
        self.assertEqual(
            word_tokenize("สวัสดีครับ สบายดีไหมครับ", engine="newmm"),
            ["สวัสดี", "ครับ", " ", "สบายดี", "ไหม", "ครับ"],
        )
        self.assertEqual(
            word_tokenize("จุ๋มง่วงนอนยัง", engine="newmm"), ["จุ๋ม", "ง่วงนอน", "ยัง"]
        )
        self.assertEqual(word_tokenize("จุ๋มง่วง", engine="newmm"), ["จุ๋ม", "ง่วง"])
        self.assertEqual(
            word_tokenize("จุ๋ม   ง่วง", engine="newmm", whitespaces=False),
            ["จุ๋ม", "ง่วง"],
        )

    def test_segment_longest_matching(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="longest"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

    def test_rank(self):
        self.assertEqual(rank(["แมว", "คน", "แมว"]), Counter({"แมว": 2, "คน": 1}))

    def test_change(self):
        self.assertEqual(texttothai("l;ylfu8iy["), "สวัสดีครับ")
        self.assertEqual(texttoeng("สวัสดีครับ"), "l;ylfu8iy[")

    def test_romanization(self):
        self.assertEqual(romanize("แมว"), "maeo")
        self.assertEqual(romanize("แมว", "pyicu"), "mæw")

    def test_romanization_royin(self):
        engine = "royin"
        self.assertEqual(romanize("แมว", engine=engine), "maeo")
        self.assertEqual(romanize("เดือน", engine=engine), "duean")
        self.assertEqual(romanize("ดู", engine=engine), "du")
        self.assertEqual(romanize("ดำ", engine=engine), "dam")
        self.assertEqual(romanize("บัว", engine=engine), "bua")

    def test_number(self):
        self.assertEqual(
            numtowords(5611116.50),
            "ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์",
        )

    def test_isthai(self):
        self.assertEqual(isthai("ประเทศไทย"), {"thai": 100.0})

    def test_tcc(self):
        self.assertEqual(tcc.tcc("ประเทศไทย"), "ป/ระ/เท/ศ/ไท/ย")

    def test_etcc(self):
        self.assertEqual(etcc.etcc("คืนความสุข"), "/คืน/ความสุข")

    def test_soundex(self):
        self.assertEqual(lk82("รถ"), "ร3000")
        self.assertEqual(udom83("รถ"), "ร800000")
        self.assertEqual(metasound("บูรณะ"), "บ550")
        self.assertEqual(metasound("คน"), "ค500")
        self.assertEqual(metasound("คนA"), "ค500")
        self.assertEqual(metasound("ดา"), "ด000")
        self.assertEqual(metasound("รักษ์"), metasound("รัก"))

    def test_wordnet(self):
        self.assertEqual(
            wordnet.synset("spy.n.01").lemma_names("tha"), ["สปาย", "สายลับ"]
        )
        self.assertIsNotNone(wordnet.langs())

    def test_spell(self):
        self.assertIsNotNone(spell("เน้ร"))
        self.assertIsNotNone(correct("ทดสอง"))

    def test_conceptnet(self):
        self.assertIsNotNone(edges("รัก"))

    def test_tnc(self):
        self.assertIsNotNone(get_word_frequency_all())

    def test_ttc(self):
        self.assertIsNotNone(ttc.get_word_frequency_all())

    def test_date(self):
        self.assertIsNotNone(now())
        self.assertEqual(reign_year_to_ad(2, 10), 2017)
        self.assertIsNotNone(reign_year_to_ad(2, 9))
        self.assertIsNotNone(reign_year_to_ad(2, 8))
        self.assertIsNotNone(reign_year_to_ad(2, 7))
        self.assertIsNotNone(now_reign_year())

    def test_summarize(self):
        text = "อาหาร หมายถึง ของแข็งหรือของเหลว "
        text += "ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว "
        text += "จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย "
        text += "ทำให้ร่างกายเจริญเติบโต "
        text += "ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย "
        text += "ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ "
        text += "อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"
        self.assertEqual(
            summarize(text=text, n=1, engine="frequency"),
            ["อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"],
        )

    def test_corpus(self):
        self.assertIsNotNone(countries())
        self.assertIsNotNone(provinces())
        self.assertIsNotNone(thai_syllables())
        self.assertIsNotNone(thai_words())
        self.assertIsNotNone(thai_stopwords())
        self.assertIsNotNone(thai_negations())

    def test_collate(self):
        self.assertEqual(collate(["ไก่", "กก"]), ["กก", "ไก่"])
        self.assertEqual(
            collate(["ไก่", "เป็ด", "หมู", "วัว"]), ["ไก่", "เป็ด", "วัว", "หมู"]
        )

    def test_normalize(self):
        self.assertEqual(normalize("เเปลก"), "แปลก")

    def test_listtext_num2num(self):
        if sys.version_info >= (3, 4):
            self.assertEqual(
                listtext_num2num(
                    ["หก", "ล้าน", "หกแสน", "หกหมื่น", "หกพัน", "หกร้อย", "หกสิบ", "หก"]
                ),
                6666666,
            )

    def test_keywords(self):
        word_list = word_tokenize(
            "แมวกินปลาอร่อยรู้ไหมว่าแมวเป็นแมวรู้ไหมนะแมว", engine="newmm"
        )
        self.assertEqual(find_keyword(word_list), {"แมว": 4})

    def test_pos_tag(self):
        self.assertEqual(
            pos_tag(word_tokenize("คุณกำลังประชุม"), engine="unigram"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
        )
        self.assertEqual(
            pos_tag_sents([["ผม", "กิน", "ข้าว"], ["แมว", "วิ่ง"]]),
            [
                [("ผม", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")],
                [("แมว", "NCMN"), ("วิ่ง", "VACT")],
            ],
        )

        if sys.version_info >= (3, 4):
            self.assertEqual(
                str(type(pos_tag(word_tokenize("ผมรักคุณ"), engine="artagger"))),
                "<class 'list'>",
            )

    def test_ner(self):
        ner = ThaiNameRecognizer()
        self.assertEqual(
            ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า"),
            [
                ("แมว", "NCMN", "O"),
                ("ทำ", "VACT", "O"),
                ("อะไร", "PNTR", "O"),
                ("ตอน", "NCMN", "O"),
                ("ห้า", "VSTA", "B-TIME"),
                ("โมง", "NCMN", "I-TIME"),
                ("เช้า", "ADVN", "I-TIME"),
            ],
        )
        self.assertEqual(
            ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False),
            [
                ("แมว", "O"),
                ("ทำ", "O"),
                ("อะไร", "O"),
                ("ตอน", "O"),
                ("ห้า", "B-TIME"),
                ("โมง", "I-TIME"),
                ("เช้า", "I-TIME"),
            ],
        )

    def test_ipa(self):
        t = ipa("คน")
        self.assertEqual(t.str(), "kʰon")
        self.assertIsNotNone(t.list())
        self.assertIsNotNone(t.xsampa_list())


if __name__ == "__main__":
    unittest.main()
