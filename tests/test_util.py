# -*- coding: utf-8 -*-
"""
Unit tests for pythainlp.util module.
"""
import os
import unittest
from collections import Counter
from datetime import datetime, time, timedelta, timezone

from pythainlp.corpus import _CORPUS_PATH, thai_words
from pythainlp.corpus.common import _THAI_WORDS_FILENAME
from pythainlp.util import (
    Trie,
    # abbreviation_to_full_text,
    arabic_digit_to_thai_digit,
    bahttext,
    collate,
    countthai,
    count_thai_chars,
    dict_trie,
    display_thai_char,
    digit_to_text,
    emoji_to_thai,
    eng_to_thai,
    find_keyword,
    is_native_thai,
    isthai,
    isthaichar,
    normalize,
    now_reign_year,
    num_to_thaiword,
    maiyamok,
    rank,
    reign_year_to_ad,
    remove_dangling,
    remove_dup_spaces,
    remove_tonemark,
    remove_zw,
    rhyme,
    text_to_arabic_digit,
    text_to_thai_digit,
    thaiword_to_date,
    thai_digit_to_arabic_digit,
    thai_strftime,
    thaiword_to_time,
    time_to_thaiword,
    thai_to_eng,
    thaiword_to_num,
    thai_keyboard_dist,
    text_to_num,
    words_to_num,
    sound_syllable,
    syllable_length,
    syllable_open_close_detector,
    tone_detector,
    thai_word_tone_detector,
    convert_years,
    thai_strptime,
    nectec_to_ipa,
    ipa_to_rtgs,
    remove_tone_ipa,
    tis620_to_utf8,
)
from pythainlp.util.spell_words import spell_word


class TestUtilPackage(unittest.TestCase):

    # ### pythainlp.util.collate

    def test_collate(self):
        self.assertEqual(collate(["ไก่", "กก"]), ["กก", "ไก่"])
        self.assertEqual(
            collate(["ไก่", "เป็ด", "หมู", "วัว"]),
            ["ไก่", "เป็ด", "วัว", "หมู"],
        )

    # ### pythainlp.util.numtoword

    def test_number(self):
        self.assertEqual(
            bahttext(5611116.50),
            "ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์",
        )
        self.assertEqual(bahttext(116), "หนึ่งร้อยสิบหกบาทถ้วน")
        self.assertEqual(bahttext(0), "ศูนย์บาทถ้วน")
        self.assertEqual(bahttext(None), "")

        self.assertEqual(num_to_thaiword(None), "")
        self.assertEqual(num_to_thaiword(0), "ศูนย์")
        self.assertEqual(num_to_thaiword(112), "หนึ่งร้อยสิบสอง")
        self.assertEqual(num_to_thaiword(-273), "ลบสองร้อยเจ็ดสิบสาม")

        self.assertEqual(thaiword_to_num("ศูนย์"), 0)
        self.assertEqual(thaiword_to_num("แปด"), 8)
        self.assertEqual(thaiword_to_num("ยี่สิบ"), 20)
        self.assertEqual(thaiword_to_num("ร้อยสิบสอง"), 112)
        self.assertEqual(
            thaiword_to_num("หกล้านหกแสนหกหมื่นหกพันหกร้อยหกสิบหก"), 6666666
        )
        self.assertEqual(thaiword_to_num("สองล้านสามแสนหกร้อยสิบสอง"), 2300612)
        self.assertEqual(thaiword_to_num("หนึ่งร้อยสิบล้าน"), 110000000)
        self.assertEqual(
            thaiword_to_num("สิบห้าล้านล้านเจ็ดสิบสอง"), 15000000000072
        )
        self.assertEqual(thaiword_to_num("หนึ่งล้านล้าน"), 1000000000000)
        self.assertEqual(
            thaiword_to_num("สองแสนสี่หมื่นสามสิบล้านสี่พันล้าน"),
            240030004000000000,
        )
        self.assertEqual(thaiword_to_num("ร้อยสิบล้านแปดแสนห้าพัน"), 110805000)
        self.assertEqual(thaiword_to_num("ลบหนึ่ง"), -1)
        text = "ลบหนึ่งร้อยล้านสี่แสนห้าพันยี่สิบเอ็ด"
        self.assertEqual(num_to_thaiword(thaiword_to_num(text)), text)
        with self.assertRaises(ValueError):
            thaiword_to_num("ศูนย์อะไรนะ")
        with self.assertRaises(ValueError):
            thaiword_to_num("")
        with self.assertRaises(ValueError):
            thaiword_to_num("ห้าพันสี่หมื่น")
        with self.assertRaises(TypeError):
            thaiword_to_num(None)
        with self.assertRaises(TypeError):
            thaiword_to_num(["หนึ่ง"])

        self.assertEqual(words_to_num("ศูนย์"), 0)
        self.assertEqual(words_to_num("แปด"), 8)
        self.assertEqual(words_to_num("ยี่สิบ"), 20)
        self.assertEqual(words_to_num("ร้อยสิบสอง"), 112)
        self.assertEqual(words_to_num("ลบแปด"), -8)
        self.assertEqual(words_to_num("ลบยี่สิบ"), -20)
        self.assertEqual(words_to_num("ลบร้อยสิบสอง"), -112)
        self.assertEqual(
            words_to_num("หกล้านหกแสนหกหมื่นหกพันหกร้อยหกสิบหก"), 6666666
        )
        self.assertEqual(words_to_num("สองล้านสามแสนหกร้อยสิบสอง"), 2300612)
        self.assertEqual(words_to_num("หนึ่งร้อยสิบล้าน"), 110000000)
        self.assertEqual(
            words_to_num("สิบห้าล้านล้านเจ็ดสิบสอง"), 15000000000072
        )
        self.assertEqual(words_to_num("หนึ่งล้านล้าน"), 1000000000000)
        self.assertEqual(
            words_to_num("สองแสนสี่หมื่นสามสิบล้านสี่พันล้าน"),
            240030004000000000,
        )
        self.assertEqual(words_to_num("ร้อยสิบล้านแปดแสนห้าพัน"), 110805000)
        self.assertEqual(words_to_num("ลบหนึ่ง"), -1)
        text = "ลบหนึ่งร้อยล้านสี่แสนห้าพันยี่สิบเอ็ด"
        self.assertEqual(num_to_thaiword(words_to_num(text)), text)
        self.assertIsNotNone(
            text_to_num("เก้าร้อยแปดสิบจุดเก้าห้าบาทนี่คือจำนวนทั้งหมด")
        )
        self.assertIsNotNone(
            text_to_num("สิบล้านสองหมื่นหนึ่งพันแปดร้อยแปดสิบเก้าบาท")
        )
        self.assertIsNotNone(
            text_to_num("สิบล้านสองหมื่นหนึ่งพันแปดร้อยแปดสิบเก้า")
        )

        self.assertEqual(
            arabic_digit_to_thai_digit("ไทยแลนด์ 4.0"), "ไทยแลนด์ ๔.๐"
        )
        self.assertEqual(arabic_digit_to_thai_digit(""), "")
        self.assertEqual(arabic_digit_to_thai_digit(None), "")

        self.assertEqual(
            thai_digit_to_arabic_digit("๔๐๔ Not Found"), "404 Not Found"
        )
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

    # ### pythainlp.util.keyboard

    def test_keyboard(self):
        self.assertEqual(eng_to_thai("l;ylfu8iy["), "สวัสดีครับ")
        self.assertEqual(
            eng_to_thai("Tok8kicsj'xitgmLwmp"), "ธนาคารแห่งประเทศไทย"
        )

        self.assertEqual(thai_to_eng("สวัสดีครับ"), "l;ylfu8iy[")
        self.assertEqual(thai_to_eng("่นีพืฟสรหท"), "journalism")
        self.assertEqual(thai_to_eng("๋นีพืฟสรหท"), "Journalism")

    # ### pythainlp.util.keywords

    def test_find_keywords(self):
        word_list = ["แมว", "กิน", "ปลา", "อร่อย", "แมว", "เป็น", "แมว"]
        self.assertEqual(find_keyword(word_list), {"แมว": 3})

    def test_rank(self):
        self.assertEqual(rank([]), None)
        self.assertEqual(
            rank(["แมว", "คน", "แมว"]), Counter({"แมว": 2, "คน": 1})
        )
        self.assertIsNotNone(
            rank(["แมว", "คน", "แมว"], exclude_stopwords=True)
        )

    # ### pythainlp.util.keyboard

    def test_thai_keyboard_dist(self):
        self.assertEqual(thai_keyboard_dist("ฟ", "ฤ"), 0.0)
        self.assertEqual(thai_keyboard_dist("ฟ", "ห"), 1.0)
        self.assertEqual(thai_keyboard_dist("ฟ", "ก"), 2.0)
        self.assertEqual(thai_keyboard_dist("ฟ", "ฤ", 0.5), 0.5)
        self.assertNotEqual(
            thai_keyboard_dist("๘", "๙"), thai_keyboard_dist("๙", "๐")
        )
        with self.assertRaises(ValueError):
            thai_keyboard_dist("ພ", "พ")

    # ### pythainlp.util.date

    def test_date(self):
        self.assertIsNotNone(now_reign_year())

        self.assertEqual(reign_year_to_ad(2, 10), 2017)
        self.assertIsNotNone(reign_year_to_ad(2, 9))
        self.assertIsNotNone(reign_year_to_ad(2, 8))
        self.assertIsNotNone(reign_year_to_ad(2, 7))

    # ### pythainlp.util.strftime

    def test_thai_strftime(self):
        date = datetime(1976, 10, 6, 1, 40, tzinfo=timezone.utc)
        self.assertEqual(thai_strftime(date, "%d"), "06")
        self.assertEqual(thai_strftime(date, "%-d"), "6")  # no padding
        self.assertEqual(thai_strftime(date, "%_d"), " 6")  # space padding
        self.assertEqual(thai_strftime(date, "%0d"), "06")  # zero padding
        self.assertEqual(thai_strftime(date, "%H"), "01")
        self.assertEqual(thai_strftime(date, "%-H"), "1")  # no padding
        self.assertEqual(thai_strftime(date, "%_M"), "40")  # space padding
        self.assertEqual(thai_strftime(date, "%0M"), "40")  # zero padding
        self.assertEqual(thai_strftime(date, "%e"), " 6")
        self.assertEqual(thai_strftime(date, "%-e"), "6")  # no padding
        self.assertEqual(thai_strftime(date, "%_e"), " 6")  # space padding
        self.assertEqual(thai_strftime(date, "%0e"), "06")  # zero padding
        self.assertEqual(thai_strftime(date, "%Ed"), "06")  # locale's alt rep
        self.assertEqual(thai_strftime(date, "%Od"), "๐๖")  # locale's numeric

        self.assertEqual(
            thai_strftime(date, "%d", thaidigit=True), "๐๖"
        )  # Thai digit
        self.assertEqual(thai_strftime(date, "%%"), "%")  # % escape
        self.assertEqual(thai_strftime(date, "%"), "%")  # one %
        self.assertEqual(thai_strftime(date, "%-"), "-")  # lone dash
        self.assertEqual(thai_strftime(date, "%c"), "พ   6 ต.ค. 01:40:00 2519")
        self.assertEqual(
            thai_strftime(date, "%0c"), "พ   6 ต.ค. 01:40:00 2519"
        )
        self.assertEqual(
            thai_strftime(date, "%c", True), "พ   ๖ ต.ค. ๐๑:๔๐:๐๐ ๒๕๑๙"
        )
        self.assertEqual(
            thai_strftime(
                date, "%Aที่ %d %B พ.ศ. %Y เวลา %H:%Mน. (%a %d-%b-%y) %% %"
            ),
            "วันพุธที่ 06 ตุลาคม พ.ศ. 2519 เวลา 01:40น. (พ 06-ต.ค.-19) % %",
        )
        self.assertEqual(thai_strftime(date, "%Q"), "Q")  # not support
        self.assertIsNotNone(
            thai_strftime(date, "%A%a%B%b%C%c%D%F%G%g%v%X%x%Y%y%+%%")
        )
        self.assertEqual(
            thai_strftime(date, "%p").upper(), thai_strftime(date, "%^p")
        )  # '^' extension for upper case
        self.assertEqual(
            thai_strftime(date, "%Z").swapcase(), thai_strftime(date, "%#Z")
        )  # '#' extension for swap case

        date = datetime(1, 2, 3)
        self.assertEqual(thai_strftime(date, "%Y"), "0544")
        self.assertEqual(thai_strftime(date, "%y"), "44")
        self.assertEqual(len(thai_strftime(date, "%G")), 4)
        self.assertEqual(len(thai_strftime(date, "%g")), 2)

    # ### pythainlp.util.time

    def test_time_to_thaiword(self):
        self.assertEqual(time_to_thaiword("8:17"), time_to_thaiword("08:17"))
        self.assertEqual(time_to_thaiword("8:17"), "แปดนาฬิกาสิบเจ็ดนาที")
        self.assertEqual(
            time_to_thaiword("8:17", "6h"), "สองโมงเช้าสิบเจ็ดนาที"
        )
        self.assertEqual(time_to_thaiword("8:17", "m6h"), "แปดโมงสิบเจ็ดนาที")
        self.assertEqual(
            time_to_thaiword("13:30:01", "6h", "m"), "บ่ายโมงครึ่ง"
        )
        self.assertEqual(
            time_to_thaiword(time(12, 3, 0)), "สิบสองนาฬิกาสามนาที"
        )
        self.assertEqual(
            time_to_thaiword(time(12, 3, 1)),
            "สิบสองนาฬิกาสามนาทีหนึ่งวินาที",
        )
        self.assertEqual(
            time_to_thaiword(datetime(2014, 5, 22, 12, 3, 0), precision="s"),
            "สิบสองนาฬิกาสามนาทีศูนย์วินาที",
        )
        self.assertEqual(
            time_to_thaiword(datetime(2014, 5, 22, 12, 3, 1), precision="m"),
            "สิบสองนาฬิกาสามนาที",
        )
        self.assertEqual(
            time_to_thaiword(datetime(1976, 10, 6, 12, 30, 1), "6h", "m"),
            "เที่ยงครึ่ง",
        )
        self.assertEqual(time_to_thaiword("18:30"), "สิบแปดนาฬิกาสามสิบนาที")
        self.assertEqual(
            time_to_thaiword("18:30:00"), "สิบแปดนาฬิกาสามสิบนาที"
        )
        self.assertEqual(
            time_to_thaiword("18:30:01"), "สิบแปดนาฬิกาสามสิบนาทีหนึ่งวินาที"
        )
        self.assertEqual(
            time_to_thaiword("18:30:01", precision="m"),
            "สิบแปดนาฬิกาสามสิบนาที",
        )
        self.assertEqual(
            time_to_thaiword("18:30:01", precision="s"),
            "สิบแปดนาฬิกาสามสิบนาทีหนึ่งวินาที",
        )
        self.assertEqual(
            time_to_thaiword("18:30:01", fmt="m6h", precision="m"),
            "หกโมงครึ่ง",
        )
        self.assertEqual(
            time_to_thaiword("18:30:01", fmt="m6h"),
            "หกโมงสามสิบนาทีหนึ่งวินาที",
        )
        self.assertEqual(
            time_to_thaiword("18:30:01", fmt="m6h", precision="m"),
            "หกโมงครึ่ง",
        )
        self.assertIsNotNone(time_to_thaiword("0:30"))
        self.assertIsNotNone(time_to_thaiword("0:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("0:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("4:30"))
        self.assertIsNotNone(time_to_thaiword("4:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("4:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("12:30"))
        self.assertIsNotNone(time_to_thaiword("12:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("12:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("13:30"))
        self.assertIsNotNone(time_to_thaiword("13:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("13:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("15:30"))
        self.assertIsNotNone(time_to_thaiword("15:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("15:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("18:30"))
        self.assertIsNotNone(time_to_thaiword("18:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("18:30", "m6h"))
        self.assertIsNotNone(time_to_thaiword("19:30"))
        self.assertIsNotNone(time_to_thaiword("19:30", "6h"))
        self.assertIsNotNone(time_to_thaiword("19:30", "m6h"))

        with self.assertRaises(NotImplementedError):
            time_to_thaiword(
                "8:17", fmt="xx"
            )  # format string is not supported
        with self.assertRaises(TypeError):
            time_to_thaiword(42)  # input is not datetime/time/str
        with self.assertRaises(ValueError):
            time_to_thaiword("")  # input is empty
        with self.assertRaises(ValueError):
            time_to_thaiword("13:73:23")  # input is not in H:M:S format
        with self.assertRaises(ValueError):
            time_to_thaiword(
                "24:00"
            )  # input is not in H:M:S format (over 23:59:59)

    def test_thaiword_to_time(self):
        self.assertEqual(thaiword_to_time("บ่ายโมงครึ่ง"), "13:30")
        self.assertEqual(thaiword_to_time("บ่ายสามโมงสิบสองนาที"), "15:12")
        self.assertEqual(thaiword_to_time("สิบโมงเช้าสิบสองนาที"), "10:12")
        self.assertEqual(thaiword_to_time("บ่ายโมงสิบสามนาที"), "13:13")
        self.assertEqual(thaiword_to_time("ศูนย์นาฬิกาสิบเอ็ดนาที"), "00:11")
        self.assertEqual(
            thaiword_to_time("บ่ายโมงเย็นสามสิบเอ็ดนาที"), "13:31"
        )
        self.assertEqual(thaiword_to_time("เที่ยงคืนหนึ่งนาที"), "00:01")
        self.assertEqual(thaiword_to_time("เที่ยงครึ่ง"), "12:30")
        self.assertEqual(thaiword_to_time("ห้าโมงเย็นสามสิบสี่นาที"), "17:34")
        self.assertEqual(thaiword_to_time("หนึ่งทุ่มสามสิบแปดนาที"), "19:38")
        self.assertEqual(thaiword_to_time("ทุ่มสามสิบแปด"), "19:38")
        self.assertEqual(
            thaiword_to_time("สองโมงเช้าสิบสองนาที", padding=False), "8:12"
        )
        self.assertEqual(thaiword_to_time("สิบโมงเช้า"), "10:00")
        self.assertEqual(thaiword_to_time("ตีสามสิบห้า"), "03:15")
        self.assertEqual(thaiword_to_time("ตีสามสิบห้านาที"), "03:15")

        with self.assertRaises(ValueError):
            thaiword_to_time("ไม่มีคำบอกเวลา")
        with self.assertRaises(ValueError):
            thaiword_to_time("นาฬิกา")

    def test_thaiword_to_date(self):
        now = datetime.now()

        self.assertEqual(
            now + timedelta(days=0), thaiword_to_date("วันนี้", now)
        )
        self.assertEqual(
            now + timedelta(days=1),
            thaiword_to_date("พรุ่งนี้", now),
        )
        self.assertEqual(
            now + timedelta(days=2),
            thaiword_to_date("มะรืนนี้", now),
        )
        self.assertEqual(
            now + timedelta(days=-1),
            thaiword_to_date("เมื่อวาน", now),
        )
        self.assertEqual(
            now + timedelta(days=-2), thaiword_to_date("วานซืน", now)
        )

        self.assertIsNotNone(thaiword_to_date("วันนี้"))

        # it's an error if "พรุ่งนี้" is 1 not 32.
        # self.assertEqual(
        #    thaiword_to_date("วันนี้").day + 1,
        #    thaiword_to_date("พรุ่งนี้").day,
        # )
        self.assertIsNone(thaiword_to_date("วันไหน"))

    # ### pythainlp.util.trie

    def test_trie(self):
        self.assertIsNotNone(Trie([]))
        self.assertIsNotNone(Trie(["ทดสอบ", "ทด", "ทอด", "ทอผ้า"]))
        self.assertIsNotNone(Trie({"ทอด", "ทอง", "ทาง"}))
        self.assertIsNotNone(Trie(("ทอด", "ทอง", "ทาง")))
        self.assertIsNotNone(Trie(Trie(["ทดสอบ", "ทดลอง"])))

        trie = Trie(["ทด", "ทดสอบ", "ทดลอง"])
        self.assertIn("ทด", trie)
        trie.add("ทบ")
        self.assertEqual(len(trie), 4)
        self.assertEqual(len(trie.prefixes("ทดสอบ")), 2)

        trie.remove("ทบ")
        trie.remove("ทด")
        self.assertEqual(len(trie), 2)

        trie = Trie([])
        self.assertEqual(len(trie), 0)
        trie.remove("หมด")
        self.assertEqual(len(trie), 0)

        self.assertIsNotNone(dict_trie(Trie(["ลอง", "ลาก"])))
        self.assertIsNotNone(dict_trie(("ลอง", "สร้าง", "Trie", "ลน")))
        self.assertIsNotNone(dict_trie(["ลอง", "สร้าง", "Trie", "ลน"]))
        self.assertIsNotNone(dict_trie({"ลอง", "สร้าง", "Trie", "ลน"}))
        self.assertIsNotNone(dict_trie(thai_words()))
        self.assertIsNotNone(
            dict_trie(os.path.join(_CORPUS_PATH, _THAI_WORDS_FILENAME))
        )
        with self.assertRaises(TypeError):
            dict_trie("")
        with self.assertRaises(TypeError):
            dict_trie(None)
        with self.assertRaises(TypeError):
            dict_trie(42)

    # ### pythainlp.util.normalize

    def test_normalize(self):
        self.assertIsNotNone(normalize("พรรค์จันทร์ab์"))

        # normalize sara e + sara e
        self.assertEqual(normalize("เเปลก"), "แปลก")

        # normalize consonant + nikhahit + sara aa
        self.assertEqual(normalize("นํา"), "นำ")
        self.assertEqual(normalize("\u0e01\u0e4d\u0e32"), "\u0e01\u0e33")

        # normalize consonant + tone mark + nikhahit + sara aa
        self.assertEqual(
            normalize("\u0e01\u0e48\u0e4d\u0e32"), "\u0e01\u0e48\u0e33"
        )

        # reorder consonant + follow vowel + tone mark
        self.assertEqual(normalize("\u0e01\u0e30\u0e48"), "\u0e01\u0e48\u0e30")

        # reorder consonant + nikhahit + tone mark + sara aa
        self.assertEqual(
            normalize("\u0e01\u0e4d\u0e48\u0e32"), "\u0e01\u0e48\u0e33"
        )

        # reorder consonant + follow vowel + tone mark
        self.assertEqual(normalize("\u0e01\u0e32\u0e48"), "\u0e01\u0e48\u0e32")

        # normalize lakkhangyao to sara aa
        self.assertEqual(normalize("นๅคา"), "นาคา")
        self.assertEqual(normalize("ฤๅษี"), "ฤๅษี")

        # remove repeating following vowels
        self.assertEqual(normalize("กาา"), "กา")
        self.assertEqual(normalize("กา า  า  า"), "กา")
        self.assertEqual(normalize("กา าาะา"), "กาะา")

        # remove repeating tone marks
        self.assertEqual(normalize("\u0e01\u0e48\u0e48"), "\u0e01\u0e48")

        # remove repeating different tone marks
        self.assertEqual(normalize("\u0e01\u0e48\u0e49"), "\u0e01\u0e49")
        self.assertEqual(
            normalize("\u0e01\u0e48\u0e49\u0e48\u0e49"), "\u0e01\u0e49"
        )

        # remove tone mark at the beginning of text
        self.assertEqual(remove_dangling("\u0e48\u0e01"), "\u0e01")
        self.assertEqual(remove_dangling("\u0e48\u0e48\u0e01"), "\u0e01")
        self.assertEqual(remove_dangling("\u0e48\u0e49\u0e01"), "\u0e01")
        self.assertEqual(remove_dangling("\u0e48\u0e01\u0e48"), "\u0e01\u0e48")

        # remove duplicate spaces
        self.assertEqual(remove_dup_spaces("  ab  c d  "), "ab c d")
        self.assertEqual(remove_dup_spaces("\nab  c   \n d \n"), "ab c\nd")

        # remove tone marks
        self.assertEqual(remove_tonemark("จิ้น"), "จิน")
        self.assertEqual(remove_tonemark("เก๋า"), "เกา")

        # remove zero width chars
        self.assertEqual(remove_zw("กา\u200b"), "กา")
        self.assertEqual(remove_zw("ก\u200cา"), "กา")
        self.assertEqual(remove_zw("\u200bกา"), "กา")
        self.assertEqual(remove_zw("กา\u200b\u200c\u200b"), "กา")

        # maiyamok
        self.assertEqual(
            maiyamok("เด็กๆชอบไปโรงเรียน"),
            ['เด็ก', 'เด็ก', 'ชอบ', 'ไป', 'โรงเรียน']
        )
        self.assertEqual(
            maiyamok([
                "ทำไม",
                "คน",
                "ดี",
                " ",
                "ๆ",
                "ๆ",
                " ",
                "ถึง",
                "ทำ",
                "ไม่ได้"
            ]),
            ["ทำไม", "คน", "ดี", "ดี", "ดี", " ", "ถึง", "ทำ", "ไม่ได้"]
        )
        self.assertEqual(
            maiyamok([
                "ทำไม",
                "คน",
                "ดี",
                " ",
                " ๆ",
                "ๆ",
                " ",
                "ถึง",
                "ทำ",
                "ไม่ได้"
            ]),
            ["ทำไม", "คน", "ดี", "ดี", "ดี", " ", "ถึง", "ทำ", "ไม่ได้"]
        )
        self.assertEqual(
            maiyamok([
                "ทำไม",
                "คน",
                "ดีๆ",
                " ",
                "ๆ",
                "ๆ",
                " ",
                "ถึง",
                "ทำ",
                "ไม่ได้"
            ]),
            ["ทำไม", "คน", "ดี", "ดี", "ดี", "ดี", " ", "ถึง", "ทำ", "ไม่ได้"]
        )

    # ### pythainlp.util.thai

    def test_countthai(self):
        self.assertEqual(countthai(""), 0.0)
        self.assertEqual(countthai("123"), 0.0)
        self.assertEqual(countthai("1 2 3"), 0.0)
        self.assertEqual(countthai("ประเทศไทย"), 100.0)
        self.assertEqual(countthai("โรค COVID-19"), 37.5)
        self.assertEqual(countthai("(กกต.)", ".()"), 100.0)
        self.assertEqual(countthai("(กกต.)", None), 50.0)

    def test_count_thai_chars(self):
        self.assertEqual(
            count_thai_chars("ทดสอบภาษาไทย"),
            {
                'vowels': 3,
                'lead_vowels': 1,
                'follow_vowels': 2,
                'above_vowels': 0,
                'below_vowels': 0,
                'consonants': 9,
                'tonemarks': 0,
                'signs': 0,
                'thai_digits': 0,
                'punctuations': 0,
                'non_thai': 0,
            }
        )
        self.assertEqual(
            count_thai_chars("มี ๕ บาทไหม๏ เกมส์หรือเกมกันแน่ที่กรุเทพฯ ใช้"),
            {
                'vowels': 12,
                'lead_vowels': 6,
                'follow_vowels': 1,
                'above_vowels': 4,
                'below_vowels': 1,
                'consonants': 22,
                'tonemarks': 3,
                'signs': 2,
                'thai_digits': 1,
                'punctuations': 1,
                'non_thai': 4,
            }
        )

    def test_isthaichar(self):
        self.assertEqual(isthaichar("ก"), True)
        self.assertEqual(isthaichar("a"), False)
        self.assertEqual(isthaichar("0"), False)

    def test_isthai(self):
        self.assertEqual(isthai("ไทย"), True)
        self.assertEqual(isthai("ไทย0"), False)
        self.assertEqual(isthai("ต.ค."), True)
        self.assertEqual(isthai("(ต.ค.)"), False)
        self.assertEqual(isthai("ต.ค.", ignore_chars=None), False)
        self.assertEqual(isthai("(ต.ค.)", ignore_chars=".()"), True)

    def test_is_native_thai(self):
        self.assertEqual(is_native_thai(None), False)
        self.assertEqual(is_native_thai(""), False)
        self.assertEqual(is_native_thai("116"), False)
        self.assertEqual(is_native_thai("abc"), False)
        self.assertEqual(is_native_thai("ตา"), True)
        self.assertEqual(is_native_thai("ยา"), True)
        self.assertEqual(is_native_thai("ฆ่า"), True)
        self.assertEqual(is_native_thai("คน"), True)
        self.assertEqual(is_native_thai("กะ"), True)
        self.assertEqual(is_native_thai("มอ"), True)
        self.assertEqual(is_native_thai("กะ"), True)
        self.assertEqual(is_native_thai("กระ"), True)
        self.assertEqual(is_native_thai("ประท้วง"), True)
        self.assertEqual(is_native_thai("ศา"), False)
        self.assertEqual(is_native_thai("ลักษ์"), False)
        self.assertEqual(is_native_thai("มาร์ค"), False)
        self.assertEqual(is_native_thai("เลข"), False)
        self.assertEqual(is_native_thai("เทเวศน์"), False)
        self.assertEqual(is_native_thai("เทเวศร์"), False)

    def test_display_thai_char(self):
        self.assertEqual(display_thai_char("้"), "_้")
        self.assertEqual(display_thai_char("ป"), "ป")
        self.assertEqual(display_thai_char("์"), "_์")
        self.assertEqual(display_thai_char("ำ"), "_ำ")
        self.assertEqual(display_thai_char("๎"), "_๎")
        self.assertEqual(display_thai_char("ํ"), "_ํ")

    # ### pythainlp.util.emojiconv

    def test_emoji_to_thai(self):
        self.assertEqual(
            emoji_to_thai(
                "จะมานั่งรถเมล์เหมือนผมก็ได้นะครับ ใกล้ชิดประชาชนดี 😀"
            ),
            (
                "จะมานั่งรถเมล์เหมือนผมก็ได้นะครับ "
                "ใกล้ชิดประชาชนดี :หน้ายิ้มยิงฟัน:"
            ),
        )
        self.assertEqual(
            emoji_to_thai("หิวข้าวอยากกินอาหารญี่ปุ่น 🍣"),
            "หิวข้าวอยากกินอาหารญี่ปุ่น :ซูชิ:",
        )
        self.assertEqual(
            emoji_to_thai("🇹🇭 นี่คือธงประเทศไทย"),
            ":ธง_ไทย: นี่คือธงประเทศไทย",
        )

    def test_sound_syllable(self):
        test = [
            ("มา", "live"),
            ("ดู", "live"),
            ("ปู", "live"),
            ("เวลา", "live"),
            ("ปี", "live"),
            ("จำ", "live"),
            ("น้ำ", "live"),
            ("ใช่", "live"),
            ("เผ่า", "live"),
            ("เสา", "live"),
            ("ไป", "live"),
            ("จริง", "live"),
            ("กิน", "live"),
            ("กำ", "live"),
            ("มา", "live"),
            ("สาว", "live"),
            ("ฉุย", "live"),
            ("ธุ", "dead"),
            ("ระ", "dead"),
            ("กะ", "dead"),
            ("ทิ", "dead"),
            ("เกะ", "dead"),
            ("กะ", "dead"),
            ("บท", "dead"),
            ("บาท", "dead"),
            ("ลาภ", "dead"),
            ("เมฆ", "dead"),
            ("เลข", "dead"),
            ("ธูป", "dead"),
            ("บ", "dead"),
            ("บ่", "dead"),
            ("ก็", "dead"),
            ("เพราะ", "dead"),
            ("เกาะ", "dead"),
            ("แคะ", "dead"),
        ]
        for i, j in test:
            self.assertEqual(sound_syllable(i), j)

    def test_tone_detector(self):
        data = [
            ("l", "กด"),
            ("l", "ต่อ"),
            ("l", "ฉาก"),
            ("l", "ใส่"),
            ("l", "อยาก"),
            ("l", "อยู่"),
            ("l", "หนวก"),
            ("l", "ใหม่"),
            ("m", "ควาย"),
            ("m", "ไป"),
            ("h", "คะ"),
            ("h", "วัด"),
            ("h", "ไม้"),
            ("h", "โต๊ะ"),
            ("r", "เขา"),
            ("r", "ก๋ง"),
            ("r", "หญิง"),
            ("f", "มาก"),
            ("f", "ใช่"),
            ("f", "ไหม้"),
            ("f", "ต้น"),
            ("f", "ผู้"),
        ]
        for i, j in data:
            self.assertEqual(tone_detector(j), i)

    def test_syllable_length(self):
        self.assertEqual(syllable_length("มาก"), "long")
        self.assertEqual(syllable_length("คะ"), "short")

    def test_syllable_open_close_detector(self):
        self.assertEqual(syllable_open_close_detector("มาก"), "close")
        self.assertEqual(syllable_open_close_detector("คะ"), "open")

    def test_thai_word_tone_detector(self):
        self.assertIsNotNone(thai_word_tone_detector("คนดี"))
        self.assertEqual(
            thai_word_tone_detector("ราคา"),
            [('รา', 'm'), ('คา', 'm')]
        )

    def test_thai_strptime(self):
        self.assertIsNotNone(
            thai_strptime(
                "05-7-65 09:00:01.10600",
                "%d-%B-%Y %H:%M:%S.%f",
                year="be"
            )
        )
        self.assertIsNotNone(
            thai_strptime(
                "24-6-75 09:00:00",
                "%d-%B-%Y %H:%M:%S",
                year="be",
                add_year="2400"
            )
        )
        self.assertIsNotNone(
            thai_strptime(
                "05-7-22 09:00:01.10600",
                "%d-%B-%Y %H:%M:%S.%f",
                year="ad"
            )
        )
        self.assertIsNotNone(
            thai_strptime(
                "05-7-99 09:00:01.10600",
                "%d-%B-%Y %H:%M:%S.%f",
                year="ad",
                add_year="1900"
            )
        )

    def test_convert_years(self):
        self.assertEqual(convert_years("2566", src="be", target="ad"), "2023")
        self.assertEqual(convert_years("2566", src="be", target="re"), "242")
        self.assertEqual(convert_years("2566", src="be", target="ah"), "1444")
        self.assertEqual(convert_years("2023", src="ad", target="be"), "2566")
        self.assertEqual(convert_years("2023", src="ad", target="ah"), "1444")
        self.assertEqual(convert_years("2023", src="ad", target="re"), "242")
        self.assertEqual(convert_years("1444", src="ah", target="be"), "2566")
        self.assertEqual(convert_years("1444", src="ah", target="ad"), "2023")
        self.assertEqual(convert_years("1444", src="ah", target="re"), "242")
        self.assertEqual(convert_years("242", src="re", target="be"), "2566")
        self.assertEqual(convert_years("242", src="re", target="ad"), "2023")
        self.assertEqual(convert_years("242", src="re", target="ah"), "1444")
        with self.assertRaises(NotImplementedError):
            self.assertIsNotNone(convert_years("2023", src="cat", target="dog"))

    def test_nectec_to_ipa(self):
        self.assertEqual(nectec_to_ipa("kl-uua-j^-2"), 'kl uua j ˥˩')

    def test_ipa_to_rtgs(self):
        self.assertEqual(ipa_to_rtgs("kluaj"), "kluai")
        self.assertEqual(ipa_to_rtgs("waːw"), "wao")
        self.assertEqual(ipa_to_rtgs("/naː˥˩/"), "/na/")

    def test_remove_tone_ipa(self):
        self.assertEqual(remove_tone_ipa("laː˦˥.sa˨˩.maj˩˩˦"), "laː.sa.maj")

    def test_tis620_to_utf8(self):
        self.assertEqual(tis620_to_utf8("¡ÃÐ·ÃÇ§ÍØµÊÒË¡ÃÃÁ"), "กระทรวงอุตสาหกรรม")

    def test_spell_word(self):
        self.assertEqual(spell_word("เสือ"),['สอ', 'เอือ', 'เสือ'])
        self.assertEqual(spell_word("เสื้อ"),['สอ', 'เอือ', 'ไม้โท', 'เสื้อ'])
        self.assertEqual(spell_word("คน"),['คอ', 'นอ', 'คน'])
        self.assertEqual(spell_word("คนดี"),['คอ', 'นอ', 'คน', 'ดอ', 'อี', 'ดี', 'คนดี'])
    
    def test_rhyme(self):
        self.assertIsInstance(rhyme("แมว"), list)
        self.assertTrue(len(rhyme("แมว")) > 2)

    # def test_abbreviation_to_full_text(self):
    #     self.assertIsInstance(abbreviation_to_full_text("รร.ของเราน่าอยู่", list))
