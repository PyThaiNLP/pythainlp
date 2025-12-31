# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.morpheme import is_native_thai, nighit


class MorphemeTestCase(unittest.TestCase):
    def test_nighit(self):
        self.assertEqual(nighit("สํ", "คีต"), "สังคีต")
        self.assertEqual(nighit("สํ", "จร"), "สัญจร")
        self.assertEqual(nighit("สํ", "ฐาน"), "สัณฐาน")
        self.assertEqual(nighit("สํ", "นิษฐาน"), "สันนิษฐาน")
        self.assertEqual(nighit("สํ", "ปทา"), "สัมปทา")
        self.assertEqual(nighit("สํ", "โยค"), "สังโยค")

    def test_is_native_thai(self):
        self.assertFalse(is_native_thai(None), False)
        self.assertFalse(is_native_thai(""), False)
        self.assertFalse(is_native_thai("116"), False)
        self.assertFalse(is_native_thai("abc"), False)
        self.assertFalse(is_native_thai("ศา"), False)
        self.assertFalse(is_native_thai("ลักษ์"), False)
        self.assertFalse(is_native_thai("มาร์ค"), False)
        self.assertFalse(is_native_thai("เลข"), False)
        self.assertFalse(is_native_thai("เทเวศน์"), False)
        self.assertFalse(is_native_thai("เทเวศร์"), False)
        self.assertTrue(is_native_thai("ตา"), True)
        self.assertTrue(is_native_thai("ยา"), True)
        self.assertTrue(is_native_thai("ฆ่า"), True)
        self.assertTrue(is_native_thai("คน"), True)
        self.assertTrue(is_native_thai("มอ"), True)
        self.assertTrue(is_native_thai("กะ"), True)
        self.assertTrue(is_native_thai("กระ"), True)
        self.assertTrue(is_native_thai("ประท้วง"), True)
