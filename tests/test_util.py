# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest
from collections import Counter

from pythainlp.util import (
    arabic_digit_to_thai_digit,
    bahttext,
    collate,
    countthai,
    deletetone,
    digit_to_text,
    eng_to_thai,
    find_keyword,
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
    thai_to_eng,
    thaicheck,
    thaiword_to_num,
)
from pythainlp.tokenize import (
    word_tokenize,
)


class TestUtilPackage(unittest.TestCase):

    # ### pythainlp.util

    def test_collate(self):
        self.assertEqual(collate(["ไก่", "กก"]), ["กก", "ไก่"])
        self.assertEqual(
            collate(["ไก่", "เป็ด", "หมู", "วัว"]),
            ["ไก่", "เป็ด", "วัว", "หมู"]
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

        self.assertEqual(thaiword_to_num("ร้อยสิบสอง"), 112)
        self.assertEqual(
            thaiword_to_num(
                ["หก", "ล้าน", "หก", "แสน", "หกหมื่น",
                 "หกพัน", "หกร้อย", "หกสิบ", "หก"]
            ),
            6666666,
        )
        self.assertEqual(thaiword_to_num("ยี่สิบ"), 20)
        self.assertEqual(thaiword_to_num("ศูนย์"), 0)
        self.assertEqual(thaiword_to_num("ศูนย์อะไรนะ"), 0)
        self.assertEqual(thaiword_to_num(""), None)
        self.assertEqual(thaiword_to_num(None), None)

        self.assertEqual(
            arabic_digit_to_thai_digit("ไทยแลนด์ 4.0"),
            "ไทยแลนด์ ๔.๐"
        )
        self.assertEqual(arabic_digit_to_thai_digit(""), "")
        self.assertEqual(arabic_digit_to_thai_digit(None), "")

        self.assertEqual(
            thai_digit_to_arabic_digit("๔๐๔ Not Found"),
            "404 Not Found"
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
            eng_to_thai("Tok8kicsj'xitgmLwmp"),
            "ธนาคารแห่งประเทศไทย"
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
            rank(["แมว", "คน", "แมว"]),
            Counter({"แมว": 2, "คน": 1})
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
        self.assertEqual(thai_strftime(date, "%c"), "พ   6 ต.ค. 01:40:00 2519")
        self.assertEqual(
            thai_strftime(date, "%c", True), "พ   ๖ ต.ค. ๐๑:๔๐:๐๐ ๒๕๑๙"
        )
        self.assertEqual(
            thai_strftime(
                date,
                "%Aที่ %d %B พ.ศ. %Y เวลา %H:%Mน. (%a %d-%b-%y) %% %"
            ),
            "วันพุธที่ 06 ตุลาคม พ.ศ. 2519 เวลา 01:40น. (พ 06-ต.ค.-19) % %",
        )
        self.assertIsNotNone(
            thai_strftime(date, "%A%a%B%b%C%c%D%F%G%g%v%X%x%Y%y%+")
        )

    # ### pythainlp.util.normalize

    def test_deletetone(self):
        self.assertEqual(deletetone("จิ้น"), "จิน")
        self.assertEqual(deletetone("เก๋า"), "เกา")

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

    def test_is_thaicheck(self):
        self.assertEqual(thaicheck("ตา"), True)
        self.assertEqual(thaicheck("ยา"), True)
        self.assertEqual(thaicheck("ฆ่า"), True)
        self.assertEqual(thaicheck("คน"), True)
        self.assertEqual(thaicheck("กะ"), True)
        self.assertEqual(thaicheck("มอ"), True)
        self.assertEqual(thaicheck("มาร์ค"), False)
        self.assertEqual(thaicheck("เลข"), False)
        self.assertEqual(thaicheck("กะ"), True)
        self.assertEqual(thaicheck("ศา"), False)
        self.assertEqual(thaicheck("abc"), False)
        self.assertEqual(thaicheck("ลักษ์"), False)
