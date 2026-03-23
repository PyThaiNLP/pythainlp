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
        self.assertEqual(spell(None), [""])  # type: ignore
        self.assertEqual(spell(""), [""])

        result = spell("เน้ร")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct(self):
        self.assertEqual(correct(None), "")  # type: ignore
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

        user_list_tuple = [
            ("การงาน", 31),  # longer than max_len
            ("กาม", 1),  # fewer than min_freq
            ("กาล0", 64),  # has digit
            ("๒๔๗๕", 64),  # has digit
            ("hello", 8),  # not Thai
            ("ลบ", -1),  # negative count
            ("การ", 42),  # OK
        ]
        checker = NorvigSpellChecker(
            custom_dict=user_list_tuple, min_freq=2, max_len=5
        )
        self.assertEqual(len(checker.dictionary()), 1)

        user_list_str = [
            "เอกราช",
            "ปลอดภัย",
            "เศรษฐกิจ",
            "เสมอภาค",
            "เสรีภาพ",
            "การศึกษา",
        ]
        checker = NorvigSpellChecker(custom_dict=user_list_str)
        self.assertEqual(len(checker.dictionary()), len(user_list_str))

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

        user_list_int = [24, 6, 2475]
        with self.assertRaises(TypeError):
            _ = NorvigSpellChecker(custom_dict=user_list_int)  # type: ignore[arg-type]

    def test_issue_680_orst_filtering(self):
        """Test for issue #680: Spell checker uses only ORST words.

        Issue #680 reported that the TNC dictionary contained misspelled words.
        The solution is to filter Phupha dataset by thai_orst_words.

        Note: Compound words like 'ปลาอินทรีย์' and 'ปลาอินทรี' that are not
        in the ORST dictionary as single entries will not be suggested by the
        spell checker. This is expected behavior when filtering to ORST words only.
        """
        from pythainlp.corpus import thai_orst_words

        checker = NorvigSpellChecker()
        orst = thai_orst_words()

        # Verify that the checker only uses ORST words
        # Check a sample of words from the dictionary
        dict_words = [word for word, _ in list(checker.dictionary())[:1000]]
        non_orst_words = [w for w in dict_words if w not in orst]
        self.assertEqual(len(non_orst_words), 0,
                        "All words in spell checker should be from ORST")

        # The specific case from issue #680
        # Both 'ปลาอินทรีย์' (misspelled) and 'ปลาอินทรี' (correct)
        # are not in ORST as compound words, so neither will be suggested
        word_misspelled = "ปลาอินทรีย์"
        word_correct = "ปลาอินทรี"

        # Verify neither is in ORST
        self.assertNotIn(word_misspelled, orst)
        self.assertNotIn(word_correct, orst)

        # Since neither is in the dictionary, the spell checker
        # will return the input word unchanged
        result = checker.correct(word_misspelled)
        # The checker returns the word as-is if no suggestions found
        self.assertEqual(result, word_misspelled)

    def test_spell_sent(self):
        self.assertIsNotNone(spell_sent(SENT_TOKS))
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="pn"))

    def test_correct_sent(self):
        self.assertIsNotNone(correct_sent(SENT_TOKS))
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="pn"))
