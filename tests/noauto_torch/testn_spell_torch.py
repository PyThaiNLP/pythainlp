# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell functions that require torch and transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch ~800MB, transformers)
# - Python 3.13+ compatibility issues
# - Long installation time

import unittest

from pythainlp.spell import (
    correct,
    correct_sent,
)

from ..core.test_spell import SENT_TOKS


class SpellWanchanbertaTestCaseN(unittest.TestCase):
    """Tests for wanchanberta_thai_grammarly engine (requires torch and transformers)"""

    def test_word_correct_wanchanberta(self):
        result = correct("ทดสอง", engine="wanchanberta_thai_grammarly")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_correct_sent_wanchanberta(self):
        self.assertIsNotNone(
            correct_sent(SENT_TOKS, engine="wanchanberta_thai_grammarly")
        )
