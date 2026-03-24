# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Test helper functions to reduce code duplication in tests.

This module provides common test assertions and patterns used across
multiple test files.
"""

import unittest


def assert_segment_handles_none_and_empty(test_case: unittest.TestCase, segment_func):
    """Test that a segment function properly handles None and empty string inputs.

    :param unittest.TestCase test_case: The unittest.TestCase instance (typically 'self')
    :param callable segment_func: The segment function to test (e.g., attacut.segment)

    :Example:
    ::

        assert_segment_handles_none_and_empty(self, attacut.segment)
    """
    test_case.assertEqual(segment_func(None), [])
    test_case.assertEqual(segment_func(""), [])


def assert_subword_tokenize_handles_none_and_empty(
    test_case: unittest.TestCase, engine: str
):
    """Test that subword_tokenize properly handles None and empty string inputs.

    :param unittest.TestCase test_case: The unittest.TestCase instance (typically 'self')
    :param str engine: The engine name to test (e.g., "phayathai")

    :Example:
    ::

        assert_subword_tokenize_handles_none_and_empty(self, "phayathai")
    """
    from pythainlp.tokenize import subword_tokenize

    test_case.assertEqual(subword_tokenize(None, engine=engine), [])  # type: ignore[arg-type]
    test_case.assertEqual(subword_tokenize("", engine=engine), [])


def assert_subword_tokenize_basic(test_case: unittest.TestCase, engine: str):
    """Run basic subword tokenize tests with common test cases.

    This helper function runs a standard set of tests for subword tokenization:

    - None input returns empty list
    - Empty string returns empty list
    - Returns list type for sample text
    - Does not produce standalone vowels

    :param unittest.TestCase test_case: The unittest.TestCase instance (typically 'self')
    :param str engine: The engine name to test

    :Example:
    ::

        assert_subword_tokenize_basic(self, "phayathai")
    """
    from pythainlp.tokenize import subword_tokenize

    # Test None and empty
    assert_subword_tokenize_handles_none_and_empty(test_case, engine)

    # Test with sample text
    test_case.assertIsInstance(
        subword_tokenize("สวัสดีดาวอังคาร", engine=engine), list
    )

    # Should not produce standalone vowels
    test_case.assertNotIn(
        "า", subword_tokenize("สวัสดีดาวอังคาร", engine=engine)
    )

    # Test with mixed Thai-numeric
    test_case.assertIsInstance(subword_tokenize("โควิด19", engine=engine), list)
