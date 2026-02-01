# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell functions that need extra dependencies
# Note: Tests requiring phunspell/tltk have been moved to tests.noautotest

import unittest

from pythainlp.spell import (
    correct,
    correct_sent,
    get_words_spell_suggestion,
    spell,
    spell_sent,
    symspellpy,
)

from ..core.test_spell import SENT_TOKS


class SpellTestCaseX(unittest.TestCase):
    def test_spell(self):
        # Tests for symspellpy only (phunspell and tltk moved to noautotest)
        result = spell("เน้ร", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct(self):
        # Tests for symspellpy only (phunspell moved to noautotest)
        result = correct("ทดสอง", engine="symspellpy")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

        result = correct("ทดสอง", engine="wanchanberta_thai_grammarly")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_spell_sent(self):
        # Tests for symspellpy only (phunspell moved to noautotest)
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="symspellpy"))

    def test_correct_sent(self):
        # Tests for symspellpy only (phunspell moved to noautotest)
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="symspellpy"))
        self.assertIsNotNone(
            correct_sent(SENT_TOKS, engine="wanchanberta_thai_grammarly")
        )
        self.assertIsNotNone(symspellpy.correct_sent(SENT_TOKS))

    def test_get_words_spell_suggestion(self):
        self.assertIsNotNone(get_words_spell_suggestion("คมดี"))
        self.assertIsNotNone(get_words_spell_suggestion(["คมดี","มะนา"]))
