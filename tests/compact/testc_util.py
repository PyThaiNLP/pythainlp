# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for pythainlp.util module.
"""

import unittest

from pythainlp.util.spell_words import spell_word


class SpellWordTestCase(unittest.TestCase):
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
