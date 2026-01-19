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
        self.assertNotIn(" cat ", prepared)
        self.assertIn("<<<PYTHAINLP_EXCLUDE_0>>>", prepared)
        self.assertEqual(
            mapping["<<<PYTHAINLP_EXCLUDE_0>>>"], "cat"
        )

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
        self.assertIn("<<<PYTHAINLP_EXCLUDE_", prepared)
        self.assertEqual(len(mapping), 2)

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
        translated = "I LOVE <<<PYTHAINLP_EXCLUDE_0>>> AND DOG"
        mapping = {"<<<PYTHAINLP_EXCLUDE_0>>>": "cat"}
        restored = _restore_excluded_words(translated, mapping)

        # Check that the word is restored
        self.assertIn("cat", restored)
        self.assertNotIn("<<<PYTHAINLP_EXCLUDE_0>>>", restored)

    def test_restore_excluded_words_multiple(self):
        """Test restoring multiple excluded words"""
        translated = (
            "<<<PYTHAINLP_EXCLUDE_0>>>กิน<<<PYTHAINLP_EXCLUDE_1>>>"
        )
        mapping = {
            "<<<PYTHAINLP_EXCLUDE_0>>>": "แมว",
            "<<<PYTHAINLP_EXCLUDE_1>>>": "ปลา",
        }
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

    def test_no_partial_match(self):
        """Test that partial word matches are not replaced"""
        text = "I love category and cat"
        exclude_words = ["cat"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # "category" should not have "cat" replaced
        self.assertIn("category", prepared)
        # Standalone "cat" should be replaced with placeholder
        # Check that "cat" as a standalone word is not in the result
        words = prepared.split()
        self.assertNotIn("cat", words)
        # The placeholder should be present
        self.assertIn("<<<PYTHAINLP_EXCLUDE_0>>>", prepared)

    def test_word_not_in_text(self):
        """Test excluding a word that doesn't appear in the text"""
        text = "I love dogs and puppies"
        exclude_words = ["cat"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Text should be unchanged since "cat" doesn't appear
        self.assertEqual(prepared, text)
        # But mapping should still exist
        self.assertEqual(len(mapping), 1)

    def test_duplicate_exclusions(self):
        """Test that duplicate words in exclusion list are handled"""
        text = "I love cat and cat"
        exclude_words = ["cat", "cat", "dog"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Should only have unique placeholders
        self.assertEqual(len(mapping), 2)  # cat and dog only
        # Both instances of "cat" should be replaced
        self.assertNotIn("cat", prepared)

    def test_overlapping_words(self):
        """Test that longer words are replaced before shorter ones"""
        text = "I have a cat and a category"
        exclude_words = ["cat", "category"]
        prepared, mapping = _prepare_text_with_exclusions(
            text, exclude_words
        )

        # Both should be replaced correctly
        self.assertNotIn("category", prepared)
        self.assertNotIn(" cat ", prepared)
        # Should have two different placeholders
        self.assertEqual(len(mapping), 2)


if __name__ == "__main__":
    unittest.main()
