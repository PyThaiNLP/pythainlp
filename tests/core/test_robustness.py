# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Robustness tests for PyThaiNLP functions.

This test suite uses strings from the Big List of Naughty Strings (BLNS)
to test the robustness, reliability, and security of PyThaiNLP functions
when handling edge cases, unusual inputs, and potentially problematic strings.

The BLNS is a list of strings which have a high probability of causing issues
when used as user-input data. More info: https://github.com/minimaxir/big-list-of-naughty-strings

We start with a small subset of categories and will gradually expand coverage.
"""

import unittest

from pythainlp.tokenize import word_tokenize
from pythainlp.util import (
    arabic_digit_to_thai_digit,
    countthai,
    isthai,
    normalize,
    remove_dup_spaces,
    thai_digit_to_arabic_digit,
)

# Thai Unicode range constants
THAI_UNICODE_START = 0x0E00
THAI_UNICODE_END = 0x0E7F


class RobustnessTestCase(unittest.TestCase):
    """Test PyThaiNLP functions with edge cases from BLNS."""

    # Category: Reserved Strings
    # Strings which may be used elsewhere in code
    RESERVED_STRINGS = [
        "undefined",
        "undef",
        "null",
        "NULL",
        "(null)",
        "nil",
        "NIL",
        "true",
        "false",
        "True",
        "False",
        "TRUE",
        "FALSE",
        "None",
        "",  # empty string
    ]

    # Category: Numeric Strings
    # Strings which can be interpreted as numeric
    NUMERIC_STRINGS = [
        "0",
        "1",
        "1.00",
        "$1.00",
        "-1",
        "-1.00",
        "1/0",
        "0/0",
        "NaN",
        "Infinity",
        "-Infinity",
        "0x0",
        "0xffffffff",
    ]

    # Category: Special Characters - ASCII punctuation
    SPECIAL_CHARS = [
        ",./;'[]\\-=",
        "<>?:\"{}|_+",
        "!@#$%^&*()`~",
    ]

    # Category: Whitespace
    # Various forms of whitespace characters
    WHITESPACE_STRINGS = [
        " ",
        "  ",
        "\t",
        "\n",
        " \t\n",
    ]

    # Category: Unicode Symbols
    UNICODE_SYMBOLS = [
        "Ω≈ç√∫˜µ≤≥÷",
        "åß∂ƒ©˙∆˚¬…æ",
        "¡™£¢∞§¶•ªº–≠",
    ]

    # Category: Thai-specific test strings
    THAI_STRINGS = [
        "สวัสดี",
        "ภาษาไทย",
        "กกกกก",
        "ก่ก้ก๊ก๋",
        "ด้้้้้็็็็็",
        "ไทย123",
        "Thai ภาษาไทย",
    ]

    # Category: Script Injection - Basic XSS
    SCRIPT_INJECTION = [
        "<script>alert(0)</script>",
        "<img src=x onerror=alert(2) />",
        "'; DROP TABLE users--",
    ]

    def test_word_tokenize_with_reserved_strings(self):
        """Test word_tokenize with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    # Should return a list
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with reserved string '{s}': {e}"
                    )

    def test_word_tokenize_with_numeric_strings(self):
        """Test word_tokenize with numeric strings."""
        for s in self.NUMERIC_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with numeric string '{s}': {e}"
                    )

    def test_word_tokenize_with_special_chars(self):
        """Test word_tokenize with special characters."""
        for s in self.SPECIAL_CHARS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with special chars '{s}': {e}"
                    )

    def test_word_tokenize_with_whitespace(self):
        """Test word_tokenize with whitespace strings."""
        for s in self.WHITESPACE_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with whitespace '{repr(s)}': {e}"
                    )

    def test_word_tokenize_with_unicode_symbols(self):
        """Test word_tokenize with unicode symbols."""
        for s in self.UNICODE_SYMBOLS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with unicode symbols '{s}': {e}"
                    )

    def test_word_tokenize_with_thai_strings(self):
        """Test word_tokenize with Thai strings."""
        for s in self.THAI_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                    # Thai text should produce at least one token
                    if s.strip():
                        self.assertGreater(len(result), 0)
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with Thai string '{s}': {e}"
                    )

    def test_word_tokenize_with_script_injection(self):
        """Test word_tokenize with script injection strings."""
        for s in self.SCRIPT_INJECTION:
            with self.subTest(input_string=s):
                try:
                    result = word_tokenize(s)
                    self.assertIsInstance(result, list)
                    # Should not execute any code, just tokenize
                except Exception as e:
                    self.fail(
                        f"word_tokenize failed with injection string '{s}': {e}"
                    )

    def test_isthai_with_reserved_strings(self):
        """Test isthai with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = isthai(s)
                    # Should return a boolean
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    self.fail(
                        f"isthai failed with reserved string '{s}': {e}"
                    )

    def test_isthai_with_numeric_strings(self):
        """Test isthai with numeric strings."""
        for s in self.NUMERIC_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = isthai(s)
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    self.fail(
                        f"isthai failed with numeric string '{s}': {e}"
                    )

    def test_countthai_with_reserved_strings(self):
        """Test countthai with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = countthai(s)
                    # Should return a number
                    self.assertIsInstance(result, (int, float))
                    self.assertGreaterEqual(result, 0)
                except Exception as e:
                    self.fail(
                        f"countthai failed with reserved string '{s}': {e}"
                    )

    def test_countthai_with_thai_strings(self):
        """Test countthai with Thai strings."""
        for s in self.THAI_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = countthai(s)
                    self.assertIsInstance(result, (int, float))
                    self.assertGreaterEqual(result, 0)
                    # Thai strings should have positive Thai character count
                    if any(
                        THAI_UNICODE_START <= ord(c) <= THAI_UNICODE_END
                        for c in s
                    ):
                        self.assertGreater(result, 0)
                except Exception as e:
                    self.fail(f"countthai failed with Thai string '{s}': {e}")

    def test_normalize_with_reserved_strings(self):
        """Test normalize with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = normalize(s)
                    # Should return a string
                    self.assertIsInstance(result, str)
                except Exception as e:
                    self.fail(
                        f"normalize failed with reserved string '{s}': {e}"
                    )

    def test_normalize_with_whitespace(self):
        """Test normalize with whitespace strings."""
        for s in self.WHITESPACE_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = normalize(s)
                    self.assertIsInstance(result, str)
                except Exception as e:
                    self.fail(
                        f"normalize failed with whitespace '{repr(s)}': {e}"
                    )

    def test_remove_dup_spaces_with_reserved_strings(self):
        """Test remove_dup_spaces with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result = remove_dup_spaces(s)
                    # Should return a string
                    self.assertIsInstance(result, str)
                except Exception as e:
                    self.fail(
                        f"remove_dup_spaces failed with reserved string '{s}': {e}"
                    )

    def test_digit_conversion_with_numeric_strings(self):
        """Test digit conversion functions with numeric strings."""
        for s in self.NUMERIC_STRINGS:
            with self.subTest(input_string=s):
                try:
                    # Test Thai digit conversion
                    result1 = arabic_digit_to_thai_digit(s)
                    self.assertIsInstance(result1, str)

                    result2 = thai_digit_to_arabic_digit(s)
                    self.assertIsInstance(result2, str)
                except Exception as e:
                    self.fail(
                        f"Digit conversion failed with numeric string '{s}': {e}"
                    )

    def test_digit_conversion_with_reserved_strings(self):
        """Test digit conversion functions with reserved strings."""
        for s in self.RESERVED_STRINGS:
            with self.subTest(input_string=s):
                try:
                    result1 = arabic_digit_to_thai_digit(s)
                    self.assertIsInstance(result1, str)

                    result2 = thai_digit_to_arabic_digit(s)
                    self.assertIsInstance(result2, str)
                except TypeError as e:
                    # The digit conversion functions raise TypeError for
                    # empty strings. This is expected behavior and documented
                    # in the function's implementation.
                    if not s:
                        pass
                    else:
                        self.fail(
                            f"Unexpected TypeError with reserved string '{s}': {e}"
                        )
                except Exception as e:
                    self.fail(
                        f"Digit conversion failed with reserved string '{s}': {e}"
                    )

    def test_functions_handle_injection_strings_safely(self):
        """
        Robustness test: Ensure functions handle injection strings without crashing.

        Note: This test verifies that text processing functions can handle
        strings containing script/SQL injection patterns without crashing.
        It does not test for actual code execution since PyThaiNLP functions
        are text processors that don't interpret HTML, JavaScript, or SQL.
        The value is in ensuring robustness against unexpected input patterns.
        """
        for s in self.SCRIPT_INJECTION:
            with self.subTest(input_string=s):
                # Test multiple functions
                try:
                    word_tokenize(s)
                    isthai(s)
                    countthai(s)
                    normalize(s)
                    # If we reach here, functions handled the input safely
                    # without crashing or executing malicious code
                except Exception as e:
                    # Functions should handle gracefully, not crash
                    self.fail(
                        f"Function crashed with injection string '{s}': {e}"
                    )
