# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell functions that need extra dependencies
# Note: Tests requiring phunspell/torch/HuggingFace Hub have been moved to tests.noauto

import unittest

from pythainlp.spell import (
    correct,
    correct_sent,
    spell,
    spell_sent,
    symspellpy,
)

from ..core.test_spell import SENT_TOKS


class SpellTestCaseX(unittest.TestCase):
    def test_spell(self):
        # Tests for symspellpy only (phunspell moved to noauto)
        result = spell("เน้ร", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์", engine="symspellpy")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct(self):
        # Tests for symspellpy only (phunspell and wanchanberta moved to noauto)
        result = correct("ทดสอง", engine="symspellpy")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_spell_sent(self):
        # Tests for symspellpy only (phunspell moved to noauto)
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="symspellpy"))

    def test_correct_sent(self):
        # Tests for symspellpy only (phunspell and wanchanberta moved to noauto)
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="symspellpy"))
        self.assertIsNotNone(symspellpy.correct_sent(SENT_TOKS))


class SpellTLTKTestCaseX(unittest.TestCase):
    """Tests for tltk engine spell checking"""

    def test_spell_tltk(self):
        result = spell("เน้ร", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เดก", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

