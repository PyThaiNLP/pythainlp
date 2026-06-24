# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.morpheme import is_native_thai, nighit


class MorphemeTestCase(unittest.TestCase):
    def test_nighit(self):
        self.assertEqual(nighit("สํ", "คีต"), "สังคีต")
        self.assertEqual(
            nighit("สํ", "คีต "), "สังคีต"
        )  # w2 has trailing space, should still work
        self.assertEqual(
            nighit("สํ ", "คีต"), "สังคีต"
        )  # w1 has trailing space, should still work
        self.assertEqual(nighit("สํ", "จร"), "สัญจร")
        self.assertEqual(nighit("สํ", "ฐาน"), "สัณฐาน")
        self.assertEqual(nighit("สํ", "นิษฐาน"), "สันนิษฐาน")
        self.assertEqual(nighit("สํ", "ปทา"), "สัมปทา")
        self.assertEqual(nighit("สํ", "โยค"), "สังโยค")
        self.assertEqual(nighit("", "คีต"), "คีต")  # w1 is empty, should return w2
        self.assertEqual(nighit("สํ", ""), "สํ")  # w2 is empty, should return w1

        with self.assertRaises(NotImplementedError):
            nighit("abc", "คีต")  # w1 does not end with ํ and len > 2
        with self.assertRaises(NotImplementedError):
            nighit("สํ", "มาร")  # consonant ม is not in any supported group
        with self.assertRaises(ValueError):
            nighit("สํ", "123")  # w2 does not contain any Thai consonant

    def test_is_native_thai(self):
        self.assertFalse(is_native_thai(None))  # type: ignore[arg-type]
        self.assertFalse(is_native_thai(""))
        self.assertFalse(is_native_thai("116"))
        self.assertFalse(is_native_thai("abc"))
        self.assertFalse(is_native_thai("ศา"))
        self.assertFalse(is_native_thai("ลักษ์"))
        self.assertFalse(is_native_thai("มาร์ค"))
        self.assertFalse(is_native_thai("เลข"))
        self.assertFalse(is_native_thai("เทเวศน์"))
        self.assertFalse(is_native_thai("เทเวศร์"))
        self.assertTrue(is_native_thai("ตา"))
        self.assertTrue(is_native_thai("ยา"))
        self.assertTrue(is_native_thai("ฆ่า"))
        self.assertTrue(is_native_thai("คน"))
        self.assertTrue(is_native_thai("มอ"))
        self.assertTrue(is_native_thai("กะ"))
        self.assertTrue(is_native_thai("กระ"))
        self.assertTrue(is_native_thai("ประท้วง"))
