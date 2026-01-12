# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for profanity detection functions
"""

import unittest

from pythainlp.corpus import thai_profanity_words
from pythainlp.util import (
    censor_profanity,
    contains_profanity,
    find_profanity,
)


class TestProfanity(unittest.TestCase):
    def test_thai_profanity_words(self):
        """Test loading profanity word list"""
        words = thai_profanity_words()
        self.assertIsInstance(words, frozenset)
        self.assertGreater(len(words), 0)

    def test_contains_profanity_clean_text(self):
        """Test clean text without profanity"""
        self.assertFalse(contains_profanity("สวัสดีครับ"))
        self.assertFalse(contains_profanity("วันนี้อากาศดีมาก"))
        self.assertFalse(contains_profanity(""))

    def test_contains_profanity_with_profanity(self):
        """Test text containing profanity"""
        # Test with actual profanity words from the list
        self.assertTrue(contains_profanity("ควย"))
        self.assertTrue(contains_profanity("สัส"))
        self.assertTrue(contains_profanity("สวัสดี ควย ครับ"))

    def test_find_profanity_clean_text(self):
        """Test finding profanity in clean text"""
        self.assertEqual(find_profanity("สวัสดีครับ"), [])
        self.assertEqual(find_profanity(""), [])

    def test_find_profanity_with_profanity(self):
        """Test finding profanity words"""
        result = find_profanity("ควย")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        result = find_profanity("สัส")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_censor_profanity_clean_text(self):
        """Test censoring clean text"""
        text = "สวัสดีครับ"
        self.assertEqual(censor_profanity(text), text)
        self.assertEqual(censor_profanity(""), "")

    def test_censor_profanity_with_profanity(self):
        """Test censoring profanity words"""
        # Test that profanity is replaced with stars
        result = censor_profanity("ควย")
        self.assertNotEqual(result, "ควย")
        self.assertIn("*", result)
        
        result = censor_profanity("สัส")
        self.assertNotEqual(result, "สัส")
        self.assertIn("*", result)

    def test_censor_profanity_custom_replacement(self):
        """Test censoring with custom replacement character"""
        result = censor_profanity("ควย", replacement="#")
        self.assertIn("#", result)
        self.assertNotIn("*", result)

    def test_contains_profanity_with_custom_words(self):
        """Test detection with custom profanity words"""
        # Clean text shouldn't be detected
        self.assertFalse(contains_profanity("สวัสดีครับ", custom_words={"คำใหม่"}))
        
        # Custom word should be detected
        self.assertTrue(contains_profanity("คำใหม่", custom_words={"คำใหม่"}))
        
        # Mix of default and custom words
        self.assertTrue(contains_profanity("ควย และ คำใหม่", custom_words={"คำใหม่"}))

    def test_find_profanity_with_custom_words(self):
        """Test finding profanity with custom words"""
        # Should find custom words
        result = find_profanity("คำใหม่", custom_words={"คำใหม่"})
        self.assertIn("คำใหม่", result)
        
        # Should find both default and custom words
        result = find_profanity("ควย และ คำใหม่", custom_words={"คำใหม่"})
        self.assertGreater(len(result), 1)

    def test_censor_profanity_with_custom_words(self):
        """Test censoring with custom profanity words"""
        # Should censor custom words
        result = censor_profanity("คำใหม่", custom_words={"คำใหม่"})
        self.assertNotEqual(result, "คำใหม่")
        self.assertIn("*", result)
        
        # Should censor both default and custom words
        result = censor_profanity("ควย และ คำใหม่", custom_words={"คำใหม่"})
        self.assertNotIn("ควย", result)
        self.assertNotIn("คำใหม่", result)
        self.assertIn("*", result)


if __name__ == "__main__":
    unittest.main()
