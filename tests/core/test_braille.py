# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.braille import thai_text_braille, thai_word_braille


class TestCase(unittest.TestCase):
    """Test Thai braille conversion."""

    def test_thai_word_braille(self) -> None:
        """Test thai_word_braille function."""
        # Test basic consonants
        self.assertEqual(thai_word_braille("กก"), "⠛⠛")
        self.assertEqual(thai_word_braille("ข"), "⠅")
        self.assertEqual(thai_word_braille("ง"), "⠻")

        # Test with vowels
        self.assertEqual(thai_word_braille("น้ำ"), "⠝⠲⠵")
        self.assertEqual(thai_word_braille("กา"), "⠛⠡")
        self.assertEqual(thai_word_braille("ดี"), "⠙⠆")

        # Test with complex words
        self.assertIsInstance(thai_word_braille("สวัสดี"), str)
        self.assertIsInstance(thai_word_braille("ครับ"), str)

        # Test empty string (should handle gracefully)
        result = thai_word_braille("")
        self.assertIsInstance(result, str)

        # Test numbers
        self.assertIsInstance(thai_word_braille("123"), str)
        self.assertIsInstance(thai_word_braille("๑๒๓"), str)

        # Additional test cases
        self.assertEqual(thai_word_braille("ลิ้น"), "⠇⠃⠲⠝")
        self.assertEqual(thai_word_braille("ว่าง"), "⠺⠔⠡⠻")
        self.assertEqual(thai_word_braille("แก้ม"), "⠣⠛⠲⠍")
        self.assertEqual(thai_word_braille("เรียน"), "⠗⠷⠝")

    def test_thai_text_braille(self) -> None:
        """Test thai_text_braille function."""
        # Test simple text - word_tokenize splits on spaces so we get 3 tokens
        result = thai_text_braille("สวัสดี ครับ")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # ['สวัสดี', ' ', 'ครับ']
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)
        self.assertIsInstance(result[2], str)

        # Test single word
        result = thai_text_braille("สวัสดี")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], str)

        # Test empty string
        result = thai_text_braille("")
        self.assertIsInstance(result, list)

        # Test text with multiple words
        result = thai_text_braille("ภาษา ไทย")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Additional test case with multiple spaces
        self.assertEqual(
            thai_text_braille("แมวกิน   ปลา"), ["⠣⠍⠺", "⠛⠃⠝", "   ", "⠯⠇⠡"]
        )
