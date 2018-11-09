# -*- coding: utf-8 -*-
import unittest
from collections import Counter
from nltk.corpus import wordnet as wn

from pythainlp.collation import collate
from pythainlp.corpus import (
    conceptnet,
    countries,
    provinces,
    remove,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
    tnc,
    ttc,
    wordnet,
)
from pythainlp.date import now, now_reign_year, reign_year_to_ad
from pythainlp.keywords import find_keyword
from pythainlp.ner import ThaiNameRecognizer
from pythainlp.ner.locations import tag_provinces
from pythainlp.number import (
    arabic_digit_to_thai_digit,
    bahttext,
    digit_to_text,
    num_to_thaiword,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
    thaiword_to_num,
)
from pythainlp.rank import rank
from pythainlp.sentiment import sentiment
from pythainlp.soundex import lk82, metasound, soundex, udom83
from pythainlp.spell import correct, spell
from pythainlp.spell.pn import NorvigSpellChecker, dictionary, known, prob
from pythainlp.summarize import summarize
from pythainlp.tag import pos_tag, pos_tag_sents
from pythainlp.tokenize import (
    FROZEN_DICT_TRIE,
    dict_word_tokenize,
    etcc,
    multi_cut,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    tcc,
    word_tokenize,
)
from pythainlp.transliterate import romanize, transliterate
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.util import (
    deletetone,
    eng_to_thai,
    is_thai,
    is_thaichar,
    is_thaiword,
    normalize,
    thai_to_eng,
)


class TestUM(unittest.TestCase):
    """
    Unit test cases
    ทดสอบการทำงาน
    """

    # ### pythainlp.collation

    def test_collate(self):
        self.assertEqual(collate(["ไก่", "กก"]), ["กก", "ไก่"])
        self.assertEqual(
            collate(["ไก่", "เป็ด", "หมู", "วัว"]), ["ไก่", "เป็ด", "วัว", "หมู"]
        )

    # ### pythainlp.corpus

    def test_conceptnet(self):
        self.assertIsNotNone(conceptnet.edges("รัก"))

    def test_corpus(self):
        self.assertIsNotNone(countries())
        self.assertIsNotNone(provinces())
        self.assertIsNotNone(thai_negations())
        self.assertIsNotNone(thai_stopwords())
        self.assertIsNotNone(thai_syllables())
        self.assertIsNotNone(thai_words())
        self.assertIsNotNone(remove("tnc_freq"))

    def test_tnc(self):
        self.assertIsNotNone(tnc.word_freqs())
        self.assertIsNotNone(tnc.word_freq("นก"))

    def test_ttc(self):
        self.assertIsNotNone(ttc.word_freqs())

    def test_wordnet(self):
        self.assertIsNotNone(wordnet.langs())

        self.assertEqual(
            wordnet.synset("spy.n.01").lemma_names("tha"), ["สปาย", "สายลับ"]
        )
        self.assertIsNotNone(wordnet.synsets("นก"))
        self.assertIsNotNone(wordnet.all_synsets(pos=wn.ADJ))

        self.assertIsNotNone(wordnet.lemmas("นก"))
        self.assertIsNotNone(wordnet.all_lemma_names(pos=wn.ADV))

        self.assertEqual(wordnet.morphy("dogs"), "dog")

    # ### pythainlp.date

    def test_date(self):
        self.assertIsNotNone(now())
        self.assertEqual(reign_year_to_ad(2, 10), 2017)
        self.assertIsNotNone(reign_year_to_ad(2, 9))
        self.assertIsNotNone(reign_year_to_ad(2, 8))
        self.assertIsNotNone(reign_year_to_ad(2, 7))
        self.assertIsNotNone(now_reign_year())

    # ### pythainlp.keywords

    def test_keywords(self):
        word_list = word_tokenize(
            "แมวกินปลาอร่อยรู้ไหมว่าแมวเป็นแมวรู้ไหมนะแมว", engine="newmm"
        )
        self.assertEqual(find_keyword(word_list), {"แมว": 4})

    # ### pythainlp.ner

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

    # ### pythainlp.ner.locations

    def test_ner_locations(self):
        self.assertEqual(
            tag_provinces(["หนองคาย", "น่าอยู่"]),
            [("หนองคาย", "B-LOCATION"), ("น่าอยู่", "O")],
        )

    # ### pythainlp.number

    def test_number(self):
        self.assertEqual(
            bahttext(5611116.50),
            "ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์",
        )
        self.assertEqual(bahttext(116), "หนึ่งร้อยสิบหกบาทถ้วน")
        self.assertEqual(bahttext(0), "ศูนย์บาทถ้วน")
        self.assertEqual(bahttext(None), "")

        self.assertEqual(num_to_thaiword(112), "หนึ่งร้อยสิบสอง")
        self.assertEqual(num_to_thaiword(0), "ศูนย์")
        self.assertEqual(num_to_thaiword(None), "")

        self.assertEqual(thaiword_to_num("ร้อยสิบสอง"), 112)
        self.assertEqual(
            thaiword_to_num(
                ["หก", "ล้าน", "หก", "แสน", "หกหมื่น", "หกพัน", "หกร้อย", "หกสิบ", "หก"]
            ),
            6666666,
        )
        self.assertEqual(thaiword_to_num("ยี่สิบ"), 20)
        self.assertEqual(thaiword_to_num("ศูนย์"), 0)
        self.assertEqual(thaiword_to_num(""), None)
        self.assertEqual(thaiword_to_num(None), None)

        self.assertEqual(arabic_digit_to_thai_digit("ไทยแลนด์ 4.0"), "ไทยแลนด์ ๔.๐")
        self.assertEqual(arabic_digit_to_thai_digit(""), "")
        self.assertEqual(arabic_digit_to_thai_digit(None), "")

        self.assertEqual(thai_digit_to_arabic_digit("๔๐๔ Not Found"), "404 Not Found")
        self.assertEqual(thai_digit_to_arabic_digit(""), "")
        self.assertEqual(thai_digit_to_arabic_digit(None), "")

        self.assertEqual(digit_to_text("RFC 7258"), "RFC เจ็ดสองห้าแปด")
        self.assertEqual(digit_to_text(""), "")
        self.assertEqual(digit_to_text(None), "")

        self.assertEqual(text_to_arabic_digit("เจ็ด"), "7")
        self.assertEqual(text_to_arabic_digit(""), "")
        self.assertEqual(text_to_arabic_digit(None), "")

        self.assertEqual(text_to_thai_digit("เก้า"), "๙")
        self.assertEqual(text_to_thai_digit(""), "")
        self.assertEqual(text_to_thai_digit(None), "")

    # ### pythainlp.rank

    def test_rank(self):
        self.assertEqual(rank([]), None)
        self.assertEqual(rank(["แมว", "คน", "แมว"]), Counter({"แมว": 2, "คน": 1}))
        self.assertIsNotNone(rank(["แมว", "คน", "แมว"], stopword=True))

    # ### pythainlp.sentiment

    def test_sentiment(self):
        text = "เสียใจมาก"
        self.assertEqual(sentiment(text, engine="old"), "neg")
        # self.assertEqual(sentiment(text, engine="ulmfit"), "neg")

    # ### pythainlp.soundex

    def test_soundex(self):
        self.assertIsNotNone(soundex("a", engine="lk82"))
        self.assertIsNotNone(soundex("a", engine="udom83"))
        self.assertIsNotNone(soundex("a", engine="metasound"))
        self.assertIsNotNone(soundex("a", engine="XXX"))

        self.assertEqual(lk82("รถ"), "ร3000")
        self.assertIsNotNone(lk82("เกาะ"))
        self.assertIsNotNone(lk82("อุยกูร์"))
        self.assertIsNotNone(lk82("หยากไย่"))
        self.assertEqual(lk82(""), "")

        self.assertEqual(udom83("รถ"), "ร800000")
        self.assertEqual(udom83(None), "")

        self.assertEqual(metasound("บูรณะ"), "บ550")
        self.assertEqual(metasound("คน"), "ค500")
        self.assertEqual(metasound("คนA"), "ค500")
        self.assertEqual(metasound("ดา"), "ด000")
        self.assertEqual(metasound("รักษ์"), metasound("รัก"))
        self.assertEqual(metasound(""), "")

    # ### pythainlp.spell

    def test_spell(self):
        self.assertIsNotNone(spell("เน้ร"))
        self.assertEqual(spell(""), "")
        self.assertEqual(spell(None), "")

        self.assertIsNotNone(correct("ทดสอง"))
        self.assertEqual(correct(""), "")
        self.assertEqual(correct(None), "")

        self.assertIsNotNone(dictionary())
        self.assertGreaterEqual(prob("มี"), 0)
        self.assertIsNotNone(known(["เกิด", "abc", ""]))

        checker = NorvigSpellChecker(dict_filter="")
        self.assertIsNotNone(checker.dictionary())
        self.assertGreaterEqual(checker.prob("มี"), 0)

    # ### pythainlp.summarize

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
        self.assertIsNotNone(summarize(text, 1, engine="XX"))

    # ### pythainlp.tag

    def test_pos_tag(self):
        tokens = ["ผม", "รัก", "คุณ"]
        self.assertIsNotNone(pos_tag(tokens, engine="unigram", corpus="orchid"))
        self.assertIsNotNone(pos_tag(tokens, engine="unigram", corpus="pud"))
        self.assertEqual(
            pos_tag(word_tokenize("คุณกำลังประชุม"), engine="unigram"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
        )

        self.assertIsNotNone(pos_tag(tokens, engine="perceptron", corpus="orchid"))
        self.assertIsNotNone(pos_tag(tokens, engine="perceptron", corpus="pud"))

        # self.assertIsNotNone(pos_tag(tokens, engine="arttagger", corpus="orchid"))
        # self.assertIsNotNone(pos_tag(tokens, engine="arttagger", corpus="pud"))

        self.assertEqual(
            pos_tag_sents([["ผม", "กิน", "ข้าว"], ["แมว", "วิ่ง"]]),
            [
                [("ผม", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")],
                [("แมว", "NCMN"), ("วิ่ง", "VACT")],
            ],
        )

    # ### pythainlp.tokenize

    def test_dict_word_tokenize(self):
        self.assertEqual(dict_word_tokenize("", custom_dict=FROZEN_DICT_TRIE), [])
        self.assertIsNotNone(
            dict_word_tokenize("รถไฟฟ้ากรุงเทพBTSหูว์ค์", custom_dict=FROZEN_DICT_TRIE)
        )
        self.assertIsNotNone(
            dict_word_tokenize(
                "รถไฟฟ้ากรุงเทพBTSหูว์ค์", custom_dict=FROZEN_DICT_TRIE, engine="newmm"
            )
        )
        self.assertIsNotNone(
            dict_word_tokenize(
                "รถไฟฟ้ากรุงเทพBTSหูว์ค์", custom_dict=FROZEN_DICT_TRIE, engine="longest"
            )
        )
        self.assertIsNotNone(
            dict_word_tokenize(
                "รถไฟฟ้ากรุงเทพBTSหูว์ค์", custom_dict=FROZEN_DICT_TRIE, engine="mm"
            )
        )
        self.assertIsNotNone(
            dict_word_tokenize(
                "รถไฟฟ้ากรุงเทพBTSหูว์ค์", custom_dict=FROZEN_DICT_TRIE, engine="XX"
            )
        )

    def test_etcc(self):
        self.assertEqual(etcc.etcc("คืนความสุข"), "/คืน/ความสุข")
        self.assertIsNotNone(
            etcc.etcc(
                "หมูแมวเหล่านี้ด้วยเหตุผลเชื่อมโยงทางกรรมพันธุ์"
                + "สัตว์มีแขนขาหน้าหัวเราะเพราะแข็งขืน"
            )
        )

    def test_word_tokenize(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )
        self.assertEqual(word_tokenize(""), [])
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="ulmfit"))
        self.assertIsNotNone(word_tokenize("ทดสอบ", engine="XX"))

    def test_word_tokenize_icu(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="icu"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )

    def test_word_tokenize_mm(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="mm"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

        self.assertIsNotNone(multi_cut.find_all_segment("รถไฟฟ้ากรุงเทพมหานครBTS"))

    def test_word_tokenize_newmm(self):
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

    def test_word_tokenize_longest_matching(self):
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="longest"),
            ["ฉัน", "รัก", "ภาษาไทย", "เพราะ", "ฉัน", "เป็น", "คนไทย"],
        )

    def test_sent_tokenize(self):
        self.assertEqual(
            sent_tokenize("รักน้ำ  รักปลา  ", engine="whitespace"), ["รักน้ำ", "รักปลา"]
        )
        self.assertEqual(sent_tokenize("รักน้ำ  รักปลา  "), ["รักน้ำ", "รักปลา"])

    def test_subword_tokenize(self):
        self.assertIsNotNone(subword_tokenize("สวัสดีดาวอังคาร"))

    def test_syllable_tokenize(self):
        self.assertEqual(
            syllable_tokenize("สวัสดีชาวโลก"), ["สวัส", "ดี", "ชาว", "โลก"]
        )

    def test_tcc(self):
        self.assertEqual(tcc.tcc("ประเทศไทย"), "ป/ระ/เท/ศ/ไท/ย")

    # ### pythainlp.transliterate

    def test_romanize(self):
        self.assertEqual(romanize("แมว"), "maeo")
        self.assertIsNotNone(romanize("กก", engine="royin"))
        self.assertEqual(romanize("แมว", engine="royin"), "maeo")
        self.assertEqual(romanize("เดือน", engine="royin"), "duean")
        self.assertEqual(romanize("ดู", engine="royin"), "du")
        self.assertEqual(romanize("ดำ", engine="royin"), "dam")
        self.assertEqual(romanize("บัว", engine="royin"), "bua")
        self.assertEqual(romanize("กร", engine="royin"), "kon")
        self.assertEqual(romanize("กรร", engine="royin"), "kan")
        self.assertEqual(romanize("กรรม", engine="royin"), "kam")
        self.assertEqual(romanize(""), "")
        self.assertEqual(romanize(None), "")
        self.assertIsNotNone(romanize("หาย", engine="royin"))
        self.assertIsNotNone(romanize("หยาก", engine="royin"))
        self.assertIsNotNone(romanize("ฝ้าย", engine="royin"))
        self.assertIsNotNone(romanize("กรม", engine="royin"))
        self.assertIsNotNone(romanize("ธรรพ์", engine="royin"))
        self.assertIsNotNone(romanize("กฏa์", engine="royin"))
        # self.assertIsNotNone(romanize("บัว", engine="thai2rom"))

    def test_transliterate(self):
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))

    # ### pythainlp.util

    def test_deletetone(self):
        self.assertEqual(deletetone("จิ้น"), "จิน")
        self.assertEqual(deletetone("เก๋า"), "เกา")

    def test_is_thai(self):
        self.assertEqual(is_thai("ประเทศไทย"), {"thai": 100.0})
        self.assertIsNotNone(is_thai("เผือก", check_all=True))

    def test_is_thaichar(self):
        self.assertEqual(is_thaichar("ก"), True)
        self.assertEqual(is_thaichar("a"), False)
        self.assertEqual(is_thaichar("0"), False)

    def test_is_thaiword(self):
        self.assertEqual(is_thaiword("ไทย"), True)
        self.assertEqual(is_thaiword("ต.ค."), True)
        self.assertEqual(is_thaiword("ไทย0"), False)

    def test_normalize(self):
        self.assertEqual(normalize("เเปลก"), "แปลก")
        self.assertIsNotNone(normalize("พรรค์จันทร์ab์"))

    def test_keyboard(self):
        self.assertEqual(eng_to_thai("l;ylfu8iy["), "สวัสดีครับ")
        self.assertEqual(thai_to_eng("สวัสดีครับ"), "l;ylfu8iy[")


if __name__ == "__main__":
    unittest.main()
