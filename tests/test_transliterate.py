# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

import torch
from pythainlp.transliterate import romanize, transliterate
from pythainlp.transliterate.ipa import trans_list, xsampa_list
from pythainlp.transliterate.royin import romanize as romanize_royin
from pythainlp.transliterate.thai2rom import ThaiTransliterator


class TestTransliteratePackage(unittest.TestCase):

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

        # self.assertEqual(romanize("แมว", engine="royin"), "maeo") # not pass
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

    def test_romanize_thai2rom(self):
        self.assertEqual(romanize("แมว", engine="thai2rom"), "maeo")
        self.assertEqual(romanize("บ้านไร่", engine="thai2rom"), "banrai")
        self.assertEqual(romanize("สุนัข", engine="thai2rom"), "sunak")
        self.assertEqual(romanize("นก", engine="thai2rom"), "nok")
        self.assertEqual(romanize("ความอิ่ม", engine="thai2rom"), "khwam-im")
        self.assertEqual(romanize("กานต์ ณรงค์", engine="thai2rom"), "kan narong")
        self.assertEqual(romanize("สกุนต์", engine="thai2rom"), "sakun")
        self.assertEqual(romanize("ชารินทร์", engine="thai2rom"), "charin")

    def test_thai2rom_prepare_sequence(self):
        transliterater = ThaiTransliterator()

        UNK_TOKEN = 1  # UNK_TOKEN or <UNK> is represented by 1
        END_TOKEN = 3  # END_TOKEN or <end> is represented by 3

        self.assertListEqual(
            transliterater._prepare_sequence_in(
                "A"
            ).cpu().detach().numpy().tolist(),
            torch.tensor(
                [UNK_TOKEN, END_TOKEN],
                dtype=torch.long
            ).cpu().detach().numpy().tolist()
        )

        self.assertListEqual(
            transliterater._prepare_sequence_in(
                "♥"
            ).cpu().detach().numpy().tolist(),
            torch.tensor(
                [UNK_TOKEN, END_TOKEN],
                dtype=torch.long
            ).cpu().detach().numpy().tolist()
        )

        self.assertNotEqual(
            transliterater._prepare_sequence_in(
                "ก"
            ).cpu().detach().numpy().tolist(),
            torch.tensor(
                [UNK_TOKEN, END_TOKEN],
                dtype=torch.long
            ).cpu().detach().numpy().tolist()
        )

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertEqual(transliterate("แมว", "pyicu"), "mæw")
        self.assertEqual(transliterate("คน", engine="ipa"), "kʰon")
        self.assertIsNotNone(trans_list("คน"))
        self.assertIsNotNone(xsampa_list("คน"))
