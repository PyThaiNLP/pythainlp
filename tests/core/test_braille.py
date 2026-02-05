# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.braille import thai_text_braille, thai_word_braille
from pythainlp.braille.core import Braille


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

        # Test edge case: characters not in mapping
        # (This should return empty string as no tokens are mappable)
        result = thai_word_braille("§")
        self.assertIsInstance(result, str)

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

    def test_braille_class(self) -> None:
        """Test Braille class methods."""
        # Test tobraille method with string input (single character)
        braille_str = Braille("1245")
        self.assertEqual(braille_str.tobraille(), "⠛")

        # Test tobraille method with list of single element
        braille_list = Braille(["1245"])
        result = braille_list.tobraille()
        self.assertIsInstance(result, str)
        # This creates ['1', '2', '4', '5'] which gives 4 separate braille chars
        self.assertGreater(len(result), 0)

        # Test tobraille method with multiple patterns (list of lists)
        # This is the structure used by thai_word_braille
        braille_multi = Braille([["1245"], ["13"]])
        result = braille_multi.tobraille()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 2)  # Two braille characters

        # Test with empty data
        braille_empty = Braille([])
        self.assertEqual(braille_empty.tobraille(), "")

        # Test with empty string
        braille_empty_str = Braille("")
        self.assertEqual(braille_empty_str.tobraille(), "")

        # Test printbraille method with string input (individual digits)
        braille_print = Braille("1245")
        result = braille_print.printbraille()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

        # Test printbraille with single-element list
        # When list has 1 element, it gets converted to sorted list of chars
        braille_print_single = Braille(["12"])
        result_single = braille_print_single.printbraille()
        self.assertIsInstance(result_single, str)
