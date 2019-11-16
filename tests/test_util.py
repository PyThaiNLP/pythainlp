# -*- coding: utf-8 -*-

import datetime
import unittest
from collections import Counter

from pythainlp.tokenize import word_tokenize
from pythainlp.util import (
    arabic_digit_to_thai_digit,
    bahttext,
    collate,
    countthai,
    delete_tone,
    deletetone,
    digit_to_text,
    eng_to_thai,
    find_keyword,
    is_native_thai,
    isthai,
    isthaichar,
    normalize,
    now_reign_year,
    num_to_thaiword,
    rank,
    reign_year_to_ad,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
    thai_strftime,
    thai_time,
    thai_to_eng,
    thaicheck,
    thaiword_to_num,
)


class TestUtilPackage(unittest.TestCase):

    # ### pythainlp.util

    def test_collate(self):
        self.assertEqual(collate(["ไก่", "กก"]), ["กก", "ไก่"])
        self.assertEqual(
            collate(["ไก่", "เป็ด", "หมู", "วัว"]),
            ["ไก่", "เป็ด", "วัว", "หมู"],
        )

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

    def test_keyboard(self):
        self.assertEqual(eng_to_thai("l;ylfu8iy["), "สวัสดีครับ")
        self.assertEqual(
            eng_to_thai("Tok8kicsj'xitgmLwmp"), "ธนาคารแห่งประเทศไทย"
        )

        self.assertEqual(thai_to_eng("สวัสดีครับ"), "l;ylfu8iy[")
        self.assertEqual(thai_to_eng("่นีพืฟสรหท"), "journalism")
        self.assertEqual(thai_to_eng("๋นีพืฟสรหท"), "Journalism")

    def test_keywords(self):
        word_list = word_tokenize(
            "แมวกินปลาอร่อยรู้ไหมว่าแมวเป็นแมวรู้ไหมนะแมว", engine="newmm"
        )
        self.assertEqual(find_keyword(word_list), {"แมว": 4})

    def test_rank(self):
        self.assertEqual(rank([]), None)
        self.assertEqual(
            rank(["แมว", "คน", "แมว"]), Counter({"แมว": 2, "คน": 1})
        )
        self.assertIsNotNone(
            rank(["แมว", "คน", "แมว"], exclude_stopwords=True)
        )

    def test_date(self):
        self.assertIsNotNone(now_reign_year())

        self.assertEqual(reign_year_to_ad(2, 10), 2017)
        self.assertIsNotNone(reign_year_to_ad(2, 9))
        self.assertIsNotNone(reign_year_to_ad(2, 8))
        self.assertIsNotNone(reign_year_to_ad(2, 7))

    def test_thai_strftime(self):
        date = datetime.datetime(1976, 10, 6, 1, 40)
        self.assertEqual(thai_strftime(date, "%d"), "06")
        # self.assertEqual(thai_strftime(date, "%-d"), "6")  # No padding
        self.assertEqual(thai_strftime(date, "%d", True), "๐๖")  # Thai digit
        self.assertEqual(thai_strftime(date, "%%"), "%")  # % escape
        self.assertEqual(thai_strftime(date, "%-"), "-")  # Lone dash
        self.assertEqual(thai_strftime(date, "%c"), "พ   6 ต.ค. 01:40:00 2519")
        self.assertEqual(
            thai_strftime(date, "%c", True), "พ   ๖ ต.ค. ๐๑:๔๐:๐๐ ๒๕๑๙"
        )
        self.assertEqual(
            thai_strftime(
                date, "%Aที่ %d %B พ.ศ. %Y เวลา %H:%Mน. (%a %d-%b-%y) %% %"
            ),
            "วันพุธที่ 06 ตุลาคม พ.ศ. 2519 เวลา 01:40น. (พ 06-ต.ค.-19) % %",
        )
        self.assertIsNotNone(
            thai_strftime(date, "%A%a%B%b%C%c%D%F%G%g%v%X%x%Y%y%+%%")
        )

    # ### pythainlp.util.thai_time

    def test_thai_time(self):
        self.assertEqual(thai_time("8:17"), thai_time("08:17"))
        self.assertEqual(thai_time("8:17"), "แปดนาฬิกาสิบเจ็ดนาที")
        self.assertEqual(thai_time("8:17", "6h"), "สองโมงเช้าสิบเจ็ดนาที")
        self.assertEqual(thai_time("8:17", "m6h"), "แปดโมงสิบเจ็ดนาที")
        self.assertEqual(thai_time("13:30:01", "6h", "m"), "บ่ายโมงครึ่ง")
        self.assertEqual(
            thai_time(datetime.time(12, 3, 0)), "สิบสองนาฬิกาสามนาที"
        )
        self.assertEqual(
            thai_time(datetime.time(12, 3, 1)),
            "สิบสองนาฬิกาสามนาทีหนึ่งวินาที",
        )
        self.assertEqual(
            thai_time(datetime.datetime(2014, 5, 22, 12, 3, 0), precision="s"),
            "สิบสองนาฬิกาสามนาทีศูนย์วินาที",
        )
        self.assertEqual(
            thai_time(datetime.datetime(2014, 5, 22, 12, 3, 1), precision="m"),
            "สิบสองนาฬิกาสามนาที",
        )
        self.assertEqual(
            thai_time(datetime.datetime(1976, 10, 6, 12, 30, 1), "6h", "m"),
            "เที่ยงครึ่ง",
        )
        self.assertEqual(thai_time("18:30"), "สิบแปดนาฬิกาสามสิบนาที")
        self.assertEqual(thai_time("18:30:00"), "สิบแปดนาฬิกาสามสิบนาที")
        self.assertEqual(
            thai_time("18:30:01"), "สิบแปดนาฬิกาสามสิบนาทีหนึ่งวินาที"
        )
        self.assertEqual(
            thai_time("18:30:01", precision="m"), "สิบแปดนาฬิกาสามสิบนาที"
        )
        self.assertEqual(
            thai_time("18:30:01", precision="s"),
            "สิบแปดนาฬิกาสามสิบนาทีหนึ่งวินาที",
        )
        self.assertEqual(
            thai_time("18:30:01", fmt="m6h", precision="m"), "หกโมงครึ่ง"
        )
        self.assertEqual(
            thai_time("18:30:01", fmt="m6h"), "หกโมงสามสิบนาทีหนึ่งวินาที"
        )
        self.assertEqual(
            thai_time("18:30:01", fmt="m6h", precision="m"), "หกโมงครึ่ง"
        )
        self.assertIsNotNone(thai_time("0:30"))
        self.assertIsNotNone(thai_time("0:30", "6h"))
        self.assertIsNotNone(thai_time("0:30", "m6h"))
        self.assertIsNotNone(thai_time("4:30"))
        self.assertIsNotNone(thai_time("4:30", "6h"))
        self.assertIsNotNone(thai_time("4:30", "m6h"))
        self.assertIsNotNone(thai_time("12:30"))
        self.assertIsNotNone(thai_time("12:30", "6h"))
        self.assertIsNotNone(thai_time("12:30", "m6h"))
        self.assertIsNotNone(thai_time("13:30"))
        self.assertIsNotNone(thai_time("13:30", "6h"))
        self.assertIsNotNone(thai_time("13:30", "m6h"))
        self.assertIsNotNone(thai_time("15:30"))
        self.assertIsNotNone(thai_time("15:30", "6h"))
        self.assertIsNotNone(thai_time("15:30", "m6h"))
        self.assertIsNotNone(thai_time("18:30"))
        self.assertIsNotNone(thai_time("18:30", "6h"))
        self.assertIsNotNone(thai_time("18:30", "m6h"))
        self.assertIsNotNone(thai_time("19:30"))
        self.assertIsNotNone(thai_time("19:30", "6h"))
        self.assertIsNotNone(thai_time("19:30", "m6h"))

        with self.assertRaises(NotImplementedError):
            thai_time("8:17", fmt="xx")

    # ### pythainlp.util.normalize

    def test_delete_tone(self):
        self.assertEqual(delete_tone("จิ้น"), "จิน")
        self.assertEqual(delete_tone("เก๋า"), "เกา")

        # Commented out until this unittest bug get fixed:
        # https://bugs.python.org/issue29620
        # with self.assertWarns(DeprecationWarning):
        #     deletetone("จิ้น")
        self.assertEqual(deletetone("จิ้น"), delete_tone("จิ้น"))

    def test_normalize(self):
        self.assertEqual(normalize("เเปลก"), "แปลก")
        self.assertIsNotNone(normalize("พรรค์จันทร์ab์"))

    # ### pythainlp.util.thai

    def test_countthai(self):
        self.assertEqual(countthai(""), 0)
        self.assertEqual(countthai("ประเทศไทย"), 100.0)
        self.assertEqual(countthai("(กกต.)", ".()"), 100.0)
        self.assertEqual(countthai("(กกต.)", None), 50.0)

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

        # Commented out until this unittest bug get fixed:
        # https://bugs.python.org/issue29620
        # with self.assertWarns(DeprecationWarning):
        #     thaicheck("เลข")
        self.assertEqual(thaicheck("เลข"), is_native_thai("เลข"))
