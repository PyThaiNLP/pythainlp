# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from pythainlp.morpheme import nighit, is_native_thai


class TestMorphemePackage(unittest.TestCase):
    def test_nighit(self):
        self.assertEqual(nighit("สํ", "คีต"), "สังคีต")
        self.assertEqual(nighit("สํ", "จร"), "สัญจร")
        self.assertEqual(nighit("สํ", "ฐาน"), "สัณฐาน")
        self.assertEqual(nighit("สํ", "นิษฐาน"), "สันนิษฐาน")
        self.assertEqual(nighit("สํ", "ปทา"), "สัมปทา")
        self.assertEqual(nighit("สํ", "โยค"), "สังโยค")

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
