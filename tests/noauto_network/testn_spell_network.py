# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for spell functions that require network access
# These tests are NOT run in automated CI workflows due to:
# - Network dependency (HuggingFace Hub downloads)
# - External service availability
# - Rate limiting concerns
# - Potential for large model downloads

import unittest

from pythainlp.spell import get_words_spell_suggestion


class SpellHuggingFaceTestCaseN(unittest.TestCase):
    """Tests for get_words_spell_suggestion (requires HuggingFace Hub network access)"""

    def test_get_words_spell_suggestion(self):
        self.assertIsNotNone(get_words_spell_suggestion("คมดี"))
        self.assertIsNotNone(get_words_spell_suggestion(["คมดี", "มะนา"]))
