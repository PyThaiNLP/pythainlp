# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Robustness tests for PyThaiNLP functions.

This test suite focuses on edge cases not covered by existing tests:
- Multi-engine robustness testing for word_tokenize
- Very long strings that can cause performance issues (issue #893)
- Thai-specific edge cases with combining characters

We avoid duplicate coverage of basic cases already tested in other test files.
"""

import unittest

from pythainlp.tokenize import word_tokenize


class RobustnessTestCase(unittest.TestCase):
    """Test PyThaiNLP functions with edge cases."""

    # Tokenization engines to test (core engines without external dependencies)
    TOKENIZE_ENGINES = ["newmm", "newmm-safe", "longest", "mm"]

    # Category: Thai-specific edge cases with combining characters
    # These test complex Thai character combinations
    THAI_EDGE_CASES = [
        "ก่ก้ก๊ก๋",  # Multiple tone marks
        "ด้้้้้็็็็็",  # Excessive combining marks
        "ไทย123English",  # Mixed scripts
        "ๆๆๆ",  # Repetition marks
        "\u200b\u200b\u200b",  # Zero-width spaces
    ]

    # Category: Very Long Strings
    # Strings that can cause performance issues or timeouts
    # Related to issue #893
    VERY_LONG_STRINGS = [
        # Long repetitive text that can cause ambiguous breaking points
        "ชิ" * 50,  # Repetitive single syllable
        "ด้านหน้า" * 20,  # Repetitive compound word
        # Mix of repetitive patterns
        "ด้านหน้า" * 10 + "กกกกกก" * 10,
    ]

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

