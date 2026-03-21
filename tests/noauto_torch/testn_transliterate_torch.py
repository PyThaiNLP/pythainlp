# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for transliteration functions that require torch
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers)
# - Python 3.13+ compatibility issues

import unittest


class TransliterateTestCaseN(unittest.TestCase):
    """Tests for transliteration functions (requires torch)"""

    def test_thai2rom_returns_string(self):
        from pythainlp.transliterate.thai2rom import romanize

        result = romanize("สวัสดี")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_thai2rom_model_loaded(self):
        from pythainlp.transliterate.thai2rom import ThaiTransliterator

        t = ThaiTransliterator()
        self.assertIsNotNone(t._network)
        self.assertIsNotNone(t._char_to_ix)
        self.assertIsNotNone(t._target_char_to_ix)
        self.assertIn("<start>", t._target_char_to_ix)
        self.assertIn("<end>", t._target_char_to_ix)

    def test_thai2rom_empty_string(self):
        from pythainlp.transliterate.thai2rom import romanize

        result = romanize("")
        self.assertIsInstance(result, str)

    def test_thaig2p_returns_string(self):
        from pythainlp.transliterate.thaig2p import transliterate

        result = transliterate("สวัสดี")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_thaig2p_model_loaded(self):
        from pythainlp.transliterate.thaig2p import ThaiG2P

        g2p = ThaiG2P()
        self.assertIsNotNone(g2p._network)
        self.assertIsNotNone(g2p._char_to_ix)
        self.assertIsNotNone(g2p._target_char_to_ix)
        self.assertIn("<start>", g2p._target_char_to_ix)
        self.assertIn("<end>", g2p._target_char_to_ix)

    def test_thaig2p_v2_returns_string(self):
        from pythainlp.transliterate.thaig2p_v2 import transliterate

        result = transliterate("สวัสดี")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_umt5_thaig2p_returns_string(self):
        from pythainlp.transliterate.umt5_thaig2p import transliterate

        result = transliterate("สวัสดี")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
