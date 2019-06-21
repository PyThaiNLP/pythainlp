# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.transliterate import romanize, transliterate
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.transliterate.royin import romanize as romanize_royin


class TestTransliteratePackage(unitest.TestCase):

    def test_romanize(self):
        self.assertEqual(romanize(None), "")
        self.assertEqual(romanize(""), "")
        self.assertEqual(romanize("แมว"), "maeo")

        self.assertEqual(romanize_royin(None), "")
        self.assertEqual(romanize_royin(""), "")
        self.assertEqual(romanize_royin("หาย"), "hai")
        self.assertEqual(romanize_royin("หมอก"), "mok")
        # self.assertEqual(romanize_royin("มหา"), "maha")  # not pass
        # self.assertEqual(romanize_royin("หยาก"), "yak")  # not pass
        # self.assertEqual(romanize_royin("อยาก"), "yak")  # not pass
        # self.assertEqual(romanize_royin("ยมก"), "yamok")  # not pass
        # self.assertEqual(romanize_royin("กลัว"), "klua")  # not pass
        # self.assertEqual(romanize_royin("กลัว"), "klua")  # not pass

        self.assertEqual(romanize("แมว", engine="royin"), "maeo")
        self.assertEqual(romanize("เดือน", engine="royin"), "duean")
        self.assertEqual(romanize("ดู", engine="royin"), "du")
        self.assertEqual(romanize("ดำ", engine="royin"), "dam")
        self.assertEqual(romanize("บัว", engine="royin"), "bua")
        self.assertEqual(romanize("กร", engine="royin"), "kon")
        self.assertEqual(romanize("กรร", engine="royin"), "kan")
        self.assertEqual(romanize("กรรม", engine="royin"), "kam")
        self.assertIsNotNone(romanize("กก", engine="royin"))
        self.assertIsNotNone(romanize("ฝ้าย", engine="royin"))
        self.assertIsNotNone(romanize("ทีปกร", engine="royin"))
        self.assertIsNotNone(romanize("กรม", engine="royin"))
        self.assertIsNotNone(romanize("ธรรพ์", engine="royin"))
        self.assertIsNotNone(romanize("กฏa์1์ ์", engine="royin"))
        self.assertEqual(romanize("แมว", engine="thai2rom"), "maeo")

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))
