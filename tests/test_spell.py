# -*- coding: utf-8 -*-

import unittest

from pythainlp.spell import NorvigSpellChecker, correct, spell


class TestSpellPackage(unittest.TestCase):

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
        self.assertTrue(len(checker.dictionary()) > 0)
        self.assertGreaterEqual(checker.prob("มี"), 0)
