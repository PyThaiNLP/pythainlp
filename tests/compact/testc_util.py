# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for pythainlp.util module."""

import unittest

from pythainlp.util import (
    check_khuap_klam,
    rhyme,
    spell_word,
    thai_word_tone_detector,
)


class SpellWordTestCaseC(unittest.TestCase):
    def test_spell_word(self):
        self.assertEqual(spell_word("เสือ"), ["สอ", "เอือ", "เสือ"])
        self.assertEqual(spell_word("เสื้อ"), ["สอ", "เอือ", "ไม้โท", "เสื้อ"])
        self.assertEqual(spell_word("คน"), ["คอ", "นอ", "คน"])
        self.assertEqual(
            spell_word("คนดี"), ["คอ", "นอ", "คน", "ดอ", "อี", "ดี", "คนดี"]
        )
        # Edge cases: None and empty string
        self.assertEqual(spell_word(None), [])
        self.assertEqual(spell_word(""), [])


class UtilTestCaseC(unittest.TestCase):
    def test_rhyme(self):
        self.assertIsInstance(rhyme("แมว"), list)
        self.assertGreater(len(rhyme("แมว")), 2)

    def test_thai_word_tone_detector(self):
        self.assertIsNotNone(thai_word_tone_detector("คนดี"))
        self.assertEqual(
            thai_word_tone_detector("ราคา"), [("รา", "m"), ("คา", "m")]
        )
        # Edge cases: None and empty string
        self.assertEqual(thai_word_tone_detector(None), [])
        self.assertEqual(thai_word_tone_detector(""), [])


class KhuapKlamTestCaseC(unittest.TestCase):
    def test_check_khuap_klam(self):
        # True consonant clusters (คำควบกล้ำแท้)
        self.assertTrue(check_khuap_klam("กราบ"))
        self.assertTrue(check_khuap_klam("ปลา"))
        self.assertTrue(check_khuap_klam("เพราะ"))
        self.assertTrue(check_khuap_klam("ตรง"))

        # False consonant clusters (คำควบกล้ำไม่แท้)
        self.assertFalse(check_khuap_klam("จริง"))
        self.assertFalse(check_khuap_klam("ทราย"))
        self.assertFalse(check_khuap_klam("เศร้า"))

        # Not a consonant cluster
        self.assertIsNone(check_khuap_klam("แม่"))
        self.assertIsNone(check_khuap_klam("ตา"))
        self.assertIsNone(check_khuap_klam("มา"))
        self.assertIsNone(check_khuap_klam("นา"))

        # Edge cases: empty string returns None
        self.assertIsNone(check_khuap_klam(""))
