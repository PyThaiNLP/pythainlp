# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.translate.core import (
    _prepare_text_with_exclusions,
    _restore_excluded_words,
)


class TestExcludeWordsHelpers(unittest.TestCase):
    """Test helper functions for word exclusion in translation"""

    def test_prepare_text_with_exclusions_single_word(self):
        """Test excluding a single word"""
        text = "I love cat and dog"
        exclude_words = ["cat"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Check that the word is replaced
        self.assertNotIn("cat", prepared)
        self.assertIn("__EXCLUDE_0__", prepared)
        self.assertEqual(mapping["__EXCLUDE_0__"], "cat")

    def test_prepare_text_with_exclusions_multiple_words(self):
        """Test excluding multiple words"""
        text = "แมวกินปลา"
        exclude_words = ["แมว", "ปลา"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Check that both words are replaced
        self.assertNotIn("แมว", prepared)
        self.assertNotIn("ปลา", prepared)
        self.assertIn("__EXCLUDE_0__", prepared)
        self.assertIn("__EXCLUDE_1__", prepared)
        self.assertEqual(mapping["__EXCLUDE_0__"], "แมว")
        self.assertEqual(mapping["__EXCLUDE_1__"], "ปลา")

    def test_prepare_text_with_exclusions_none(self):
        """Test with no exclusions"""
        text = "Hello world"
        exclude_words = None
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Text should be unchanged
        self.assertEqual(prepared, text)
        self.assertEqual(mapping, {})

    def test_prepare_text_with_exclusions_empty_list(self):
        """Test with empty exclusion list"""
        text = "Hello world"
        exclude_words = []
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Text should be unchanged
        self.assertEqual(prepared, text)
        self.assertEqual(mapping, {})

    def test_restore_excluded_words(self):
        """Test restoring excluded words"""
        translated = "I LOVE __EXCLUDE_0__ AND DOG"
        mapping = {"__EXCLUDE_0__": "cat"}
        restored = _restore_excluded_words(translated, mapping)

        # Check that the word is restored
        self.assertIn("cat", restored)
        self.assertNotIn("__EXCLUDE_0__", restored)

    def test_restore_excluded_words_multiple(self):
        """Test restoring multiple excluded words"""
        translated = "__EXCLUDE_0__กิน__EXCLUDE_1__"
        mapping = {"__EXCLUDE_0__": "แมว", "__EXCLUDE_1__": "ปลา"}
        restored = _restore_excluded_words(translated, mapping)

        # Check that both words are restored
        self.assertEqual(restored, "แมวกินปลา")

    def test_restore_excluded_words_empty_map(self):
        """Test restoring with empty mapping"""
        translated = "Hello world"
        mapping = {}
        restored = _restore_excluded_words(translated, mapping)

        # Text should be unchanged
        self.assertEqual(restored, translated)

    def test_roundtrip(self):
        """Test full roundtrip of prepare and restore"""
        original = "I love cat and dog"
        exclude_words = ["cat"]

        # Prepare
        prepared, mapping = _prepare_text_with_exclusions(
            original, exclude_words
        )

        # Simulate translation (just uppercase)
        translated = prepared.upper()

        # Restore
        restored = _restore_excluded_words(translated, mapping)

        # Check that the excluded word is preserved
        self.assertIn("cat", restored)
        # Other words should be uppercase
        self.assertIn("I LOVE", restored)
        self.assertIn("AND DOG", restored)


if __name__ == "__main__":
    unittest.main()
