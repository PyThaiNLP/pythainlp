# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.spell import (
    NorvigSpellChecker,
    correct,
    correct_sent,
    spell,
    spell_sent,
)

SENT_TOKS = ["เด็", "อินอร์เน็ต", "แรง"]


class SpellTestCase(unittest.TestCase):
    def test_spell(self):
        self.assertEqual(spell(None), [""])
        self.assertEqual(spell(""), [""])

        result = spell("เน้ร")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct(self):
        self.assertEqual(correct(None), "")
        self.assertEqual(correct(""), "")
        self.assertEqual(correct("1"), "1")
        self.assertEqual(correct("05"), "05")
        self.assertEqual(correct("56"), "56")
        self.assertEqual(correct("1.01"), "1.01")

        result = correct("ทดสอง")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_norvig_spell_checker(self):
        checker = NorvigSpellChecker(dict_filter=None)
        self.assertGreater(len(checker.dictionary()), 0)
        self.assertGreaterEqual(checker.prob("มี"), 0)

        # Verify default dictionary is filtered with thai_orst_words
        from pythainlp.corpus import thai_orst_words
        orst = thai_orst_words()
        # Check that dictionary size is reasonable (around ORST size)
        dict_size = len(checker.dictionary())
        self.assertGreater(dict_size, 30000)  # Should have substantial words
        self.assertLess(dict_size, len(orst) + 1000)  # Should not exceed ORST by much

        user_dict = [
            ("การงาน", 31),  # longer than max_len
            ("กาม", 1),  # fewer than min_freq
            ("กาล0", 64),  # has digit
            ("๒๔๗๕", 64),  # has digit
            ("hello", 8),  # not Thai
            ("ลบ", -1),  # negative count
            ("การ", 42),  # OK
        ]
        checker = NorvigSpellChecker(
            custom_dict=user_dict, min_freq=2, max_len=5
        )
        self.assertEqual(len(checker.dictionary()), 1)

        user_dict = [
            "เอกราช",
            "ปลอดภัย",
            "เศรษฐกิจ",
            "เสมอภาค",
            "เสรีภาพ",
            "การศึกษา",
        ]
        checker = NorvigSpellChecker(custom_dict=user_dict)
        self.assertEqual(len(checker.dictionary()), len(user_dict))

        user_dict = {
            "พหลโยธิน": 1,
            "ขีตตะสังคะ": 2,
            "พนมยงค์": 3,
            "ภมรมนตรี": 4,
            "มิตรภักดี": 5,
            "ลพานุกรม": 6,
            "สิงหเสนี": 7,
        }
        checker = NorvigSpellChecker(custom_dict=user_dict)
        # "พหลโยธิน" will be removed,
        # as it has frequency less than default min_freq (2)
        self.assertEqual(len(checker.dictionary()), len(user_dict) - 1)

        user_dict = [24, 6, 2475]
        with self.assertRaises(TypeError):
            _ = NorvigSpellChecker(custom_dict=user_dict)

    def test_spell_sent(self):
        self.assertIsNotNone(spell_sent(SENT_TOKS))
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="pn"))

    def test_correct_sent(self):
        self.assertIsNotNone(correct_sent(SENT_TOKS))
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="pn"))
