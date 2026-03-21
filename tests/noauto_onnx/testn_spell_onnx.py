# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell correction functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime)
# - Platform-specific compatibility issues
# - Version constraints

import unittest


class SpellONNXTestCaseN(unittest.TestCase):
    """Tests for ONNX-based spell correction (requires onnxruntime)"""

    def test_words_spelling_correction_returns_list(self):
        from pythainlp.spell.words_spelling_correction import (
            get_words_spell_suggestion,
        )

        result = get_words_spell_suggestion("สวัสดี")
        self.assertIsInstance(result, list)

    def test_words_spelling_correction_nonempty_input(self):
        from pythainlp.spell.words_spelling_correction import (
            get_words_spell_suggestion,
        )

        result = get_words_spell_suggestion("กาารเขียน")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_words_spelling_correction_items_are_strings(self):
        from pythainlp.spell.words_spelling_correction import (
            get_words_spell_suggestion,
        )

        result = get_words_spell_suggestion("กาารเขียน")
        for item in result:
            self.assertIsInstance(item, str)
