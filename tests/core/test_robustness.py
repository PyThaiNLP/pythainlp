# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Robustness tests for PyThaiNLP functions.

This test suite focuses on edge cases important for real-world usage:
- Empty strings and various whitespace handling
- Special characters from terminal copy/paste and encoding issues
- Unicode edge cases (truncated, BOM, control characters)
- Emoji and hidden/invisible characters
- Multi-engine robustness testing for word_tokenize
- Very long strings that can cause performance issues (issue #893)
"""

import unittest

from pythainlp.tokenize import word_tokenize


class RobustnessTestCase(unittest.TestCase):
    """Test PyThaiNLP functions with edge cases."""

    # Tokenization engines to test (core engines without external dependencies)
    TOKENIZE_ENGINES = ["newmm", "newmm-safe", "longest", "mm"]

    # Category: Empty and Whitespace strings
    # Real-world cases from copy/paste, terminal input, etc.
    EMPTY_AND_WHITESPACE = [
        "",  # Empty string
        " ",  # Single space
        "  ",  # Multiple spaces
        "\t",  # Tab
        "\n",  # Newline
        "\r\n",  # Windows line ending
        " \t\n\r",  # Mixed whitespace
        "\u00a0",  # Non-breaking space
        "\u2000\u2001\u2002",  # Various unicode spaces
        "\u3000",  # Ideographic space (CJK)
    ]

    # Category: Special characters from encoding issues and terminal
    # BOM, control characters, special punctuation
    SPECIAL_CHARS = [
        "\ufeff",  # BOM (Byte Order Mark)
        "\ufffe",  # BOM reversed
        "\x00",  # Null character
        "\u0000",  # Null unicode
        "‌‍",  # Zero-width non-joiner, zero-width joiner
        "\u200c\u200d",  # ZWNJ, ZWJ
        "\u200e\u200f",  # LTR mark, RTL mark
        "­",  # Soft hyphen
        "\u00ad",  # Soft hyphen unicode
        "…",  # Ellipsis
        "—–-",  # Different dashes
        "\u201c\u201d",  # Smart double quotes (curly quotes)
        "\u2018\u2019",  # Smart single quotes (curly quotes)
    ]

    # Category: Truncated/malformed Unicode
    # Characters that might be cut in the middle of encoding
    TRUNCATED_UNICODE = [
        "\ud800",  # High surrogate alone (invalid)
        "\udc00",  # Low surrogate alone (invalid)
        "test\ud800text",  # High surrogate in middle
        "สวัสดี\udc00",  # Thai with low surrogate
    ]

    # Category: Emoji and Modern Unicode
    # Emoji, emoji sequences, and variations
    EMOJI_CASES = [
        "😀",  # Basic emoji
        "👨‍👩‍👧‍👦",  # Family emoji (ZWJ sequence)
        "👍🏻",  # Emoji with skin tone modifier
        "🇹🇭",  # Flag (regional indicator symbols)
        "😀😃😄",  # Multiple emoji
        "สวัสดี😀ครับ",  # Thai text with emoji
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿",  # Flag with tag sequences
    ]

    # Category: Control and Hidden Characters
    # Characters that don't display but affect processing
    CONTROL_AND_HIDDEN = [
        "\x01\x02\x03",  # Control characters
        "\u0001\u0002\u0003",  # Control chars unicode
        "\u200b",  # Zero-width space
        "\u200c",  # Zero-width non-joiner
        "\u200d",  # Zero-width joiner
        "\ufeff",  # Zero-width no-break space (BOM)
        "test\u200bword",  # Text with zero-width space
        "ภาษา\u200cไทย",  # Thai with ZWNJ
        "\u034f",  # Combining grapheme joiner
    ]

    # Category: Thai-specific edge cases with combining characters
    THAI_EDGE_CASES = [
        "ก่ก้ก๊ก๋",  # Multiple tone marks
        "ด้้้้้็็็็็",  # Excessive combining marks
        "ไทย123English",  # Mixed scripts
        "ๆๆๆ",  # Repetition marks
        "\u200b\u200b\u200b",  # Zero-width spaces
    ]

    # Category: Very Long Strings (issue #893)
    VERY_LONG_STRINGS = [
        "ชิ" * 50,  # Repetitive single syllable
        "ด้านหน้า" * 20,  # Repetitive compound word
        "ด้านหน้า" * 10 + "กกกกกก" * 10,  # Mixed patterns
    ]

    def test_word_tokenize_empty_and_whitespace(self):
        """
        Test word_tokenize with empty strings and various whitespace.

        These cases are common in real-world usage from copy/paste,
        terminal input, and various text processing scenarios.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.EMPTY_AND_WHITESPACE:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                    except Exception as e:
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"whitespace case {repr(s)}: {e}"
                        )

    def test_word_tokenize_special_chars(self):
        """
        Test word_tokenize with special characters.

        Tests BOM, control characters, zero-width characters, and special
        punctuation that often appear from encoding issues or terminal copy/paste.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.SPECIAL_CHARS:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                    except Exception as e:
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"special char {repr(s)}: {e}"
                        )

    def test_word_tokenize_truncated_unicode(self):
        """
        Test word_tokenize with truncated or malformed Unicode.

        Tests handling of surrogate pairs and characters that might be
        cut in the middle of multi-byte encoding.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.TRUNCATED_UNICODE:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                    except Exception as e:
                        # Truncated unicode might cause issues, but shouldn't crash
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"truncated unicode {repr(s)}: {e}"
                        )

    def test_word_tokenize_emoji(self):
        """
        Test word_tokenize with emoji and modern Unicode sequences.

        Tests emoji, emoji with modifiers, ZWJ sequences, and flags.
        Important for modern text processing.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.EMOJI_CASES:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                        if s.strip():
                            self.assertGreater(len(result), 0)
                    except Exception as e:
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"emoji {repr(s)}: {e}"
                        )

    def test_word_tokenize_control_and_hidden(self):
        """
        Test word_tokenize with control and hidden characters.

        Tests zero-width characters, control characters, and other
        invisible characters that affect text processing.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.CONTROL_AND_HIDDEN:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                    except Exception as e:
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"control/hidden char {repr(s)}: {e}"
                        )

    def test_word_tokenize_thai_edge_cases_multi_engine(self):
        """
        Test word_tokenize with Thai edge cases across multiple engines.

        Tests complex Thai character combinations including excessive combining
        marks, mixed scripts, and special characters across all core engines
        to ensure consistent handling.
        """
        for engine in self.TOKENIZE_ENGINES:
            for s in self.THAI_EDGE_CASES:
                with self.subTest(engine=engine, input_string=repr(s)):
                    try:
                        result = word_tokenize(s, engine=engine)
                        self.assertIsInstance(result, list)
                        # Non-empty input should produce at least one token
                        if s.strip():
                            self.assertGreater(len(result), 0)
                    except Exception as e:
                        self.fail(
                            f"word_tokenize (engine={engine}) failed with "
                            f"Thai edge case {repr(s)}: {e}"
                        )

    def test_word_tokenize_with_very_long_strings(self):
        """
        Test word_tokenize with very long strings.

        This test addresses issue #893 - testing tokenization performance
        and robustness with very long strings, including repetitive patterns
        that can cause ambiguous breaking points and long processing times.

        Uses newmm-safe engine which is designed to handle such cases.
        """
        # Use newmm-safe which has safeguards against long processing times
        engine = "newmm-safe"
        for i, s in enumerate(self.VERY_LONG_STRINGS):
            with self.subTest(engine=engine, string_index=i):
                try:
                    result = word_tokenize(s, engine=engine)
                    self.assertIsInstance(result, list)
                    # Very long strings should still produce tokens
                    self.assertGreater(len(result), 0)
                except Exception as e:
                    self.fail(
                        f"word_tokenize (engine={engine}) failed with "
                        f"very long string (index={i}): {e}"
                    )

