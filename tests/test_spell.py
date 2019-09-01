# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.spell import NorvigSpellChecker, correct, spell


class TestSpellPackage(unittest.TestCase):

    def test_spell(self):
        self.assertEqual(spell(None), "")
        self.assertEqual(spell(""), "")
        self.assertIsNotNone(spell("เน้ร"))
        self.assertIsNotNone(spell("เกสมร์"))

        self.assertEqual(correct(None), "")
        self.assertEqual(correct(""), "")
        self.assertIsNotNone(correct("ทดสอง"))

        checker = NorvigSpellChecker(dict_filter="")
        self.assertIsNotNone(checker.dictionary())
        self.assertGreaterEqual(checker.prob("มี"), 0)
