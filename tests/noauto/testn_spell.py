# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell functions that require phunspell (Cython) or tltk
# These tests are NOT run in automated CI workflows due to:
# - Compilation issues (phunspell requires Cython)
# - Compilation issues (tltk)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.spell import (
    correct,
    correct_sent,
    spell,
    spell_sent,
)

from ..core.test_spell import SENT_TOKS


class SpellPhunspellTestCaseN(unittest.TestCase):
    """Tests for phunspell engine (requires Cython compilation)"""

    def test_spell_phunspell(self):
        result = spell("เน้ร", engine="phunspell")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เกสมร์", engine="phunspell")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_word_correct_phunspell(self):
        result = correct("ทดสอง", engine="phunspell")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_spell_sent_phunspell(self):
        self.assertIsNotNone(spell_sent(SENT_TOKS, engine="phunspell"))

    def test_correct_sent_phunspell(self):
        self.assertIsNotNone(correct_sent(SENT_TOKS, engine="phunspell"))


class SpellTLTKTestCaseN(unittest.TestCase):
    """Tests for tltk engine (requires tltk with compilation issues)"""

    def test_spell_tltk(self):
        result = spell("เน้ร", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        result = spell("เดก", engine="tltk")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
