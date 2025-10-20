# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.spell import (
    correct,
    correct_sent,
    spell,
    spell_sent,
    symspellpy,
    get_words_spell_suggestion,
)

from ..core.test_spell import SENT_TOKS


class SpellTestCaseX(unittest.TestCase):
    def test_spell(self):
        result = spell("เน้ร", engine="phunspell")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์", engine="phunspell")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เน้ร", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เน้ร", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เดก", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct(self):
        result = correct("ทดสอง", engine="phunspell")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

        result = correct("ทดสอง", engine="symspellpy")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

        result = correct("ทดสอง", engine="wanchanberta_thai_grammarly")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_spell_sent(self):
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="phunspell"))
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="symspellpy"))

    def test_correct_sent(self):
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="phunspell"))
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="symspellpy"))
        self.assertIsNotNone(
            correct_sent(SENT_TOKS, engine="wanchanberta_thai_grammarly")
        )
        self.assertIsNotNone(symspellpy.correct_sent(SENT_TOKS))

    def test_get_words_spell_suggestion(self):
        self.assertIsNotNone(get_words_spell_suggestion("คมดี"))
        self.assertIsNotNone(get_words_spell_suggestion(["คมดี","มะนา"]))
