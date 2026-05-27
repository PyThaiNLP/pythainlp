# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Correctness and performance tests for Cython-compiled fast functions.

These tests verify that the Cython implementations in pythainlp._ext produce
identical output to the pure Python implementations they replace.

Tests are skipped automatically when the Cython extensions are not built
(e.g., on PyPy or systems without a C compiler).
"""

import unittest

try:
    from pythainlp._ext._normalize_fast import (
        remove_dup_spaces as fast_remove_dup_spaces,
    )
    from pythainlp._ext._normalize_fast import (
        remove_tonemark as fast_remove_tonemark,
    )
    from pythainlp._ext._thai_fast import (
        count_thai as fast_count_thai,
    )
    from pythainlp._ext._thai_fast import (
        is_thai as fast_is_thai,
    )
    from pythainlp._ext._thai_fast import (
        is_thai_char as fast_is_thai_char,
    )

    HAVE_EXT = True
except ImportError:
    HAVE_EXT = False


class FastThaiCharCorrectnessTest(unittest.TestCase):
    """Verify Cython _thai_fast functions match Python implementations."""

    def setUp(self) -> None:
        if not HAVE_EXT:
            self.skipTest(
                "pythainlp._ext Cython extensions not built; skipping"
            )

    def test_is_thai_char_thai(self) -> None:
        for ch in ["ก", "ข", "ค", "๑", "฿", "ๆ", "ๅ"]:
            with self.subTest(ch=ch):
                self.assertTrue(fast_is_thai_char(ch))

    def test_is_thai_char_non_thai(self) -> None:
        for ch in ["a", "Z", "0", "9", " ", "あ", "中", "€"]:
            with self.subTest(ch=ch):
                self.assertFalse(fast_is_thai_char(ch))

    def test_is_thai_char_boundary(self) -> None:
        # First and last code points in the Thai Unicode block
        self.assertTrue(fast_is_thai_char(chr(0x0E00)))
        self.assertTrue(fast_is_thai_char(chr(0x0E7F)))
        # Just outside the Thai block
        self.assertFalse(fast_is_thai_char(chr(0x0DFF)))
        self.assertFalse(fast_is_thai_char(chr(0x0E80)))

    def test_is_thai_char_empty(self) -> None:
        self.assertFalse(fast_is_thai_char(""))

    def test_is_thai_char_matches_python(self) -> None:
        # Use the pure-Python reference saved before the Cython override runs.
        # Empty string is excluded: Python's ord("") raises TypeError while
        # Cython returns False — this known difference is covered separately
        # in test_is_thai_char_empty.
        from pythainlp.util.thai import _py_is_thai_char as py_is_thai_char

        test_chars = [
            "ก",
            "ข",
            "ค",
            "a",
            "1",
            " ",
            chr(0x0E00),
            chr(0x0E7F),
            chr(0x0DFF),
            chr(0x0E80),
            "あ",
        ]
        for ch in test_chars:
            with self.subTest(ch=repr(ch)):
                self.assertEqual(
                    fast_is_thai_char(ch),
                    py_is_thai_char(ch),
                    f"Mismatch for {repr(ch)}",
                )

    def test_is_thai_matches_python(self) -> None:
        from pythainlp.util.thai import _py_is_thai as py_is_thai

        test_cases = [
            ("ทดสอบ", "."),
            ("ทดสอบ1", "."),
            ("hello", "."),
            ("ทดสอบ123", "123"),
            ("", "."),
            ("ก.", "."),
        ]
        for text, ignore in test_cases:
            with self.subTest(text=repr(text)):
                self.assertEqual(
                    fast_is_thai(text, ignore),
                    py_is_thai(text, ignore),
                    f"Mismatch for {repr(text)!r}, ignore={repr(ignore)!r}",
                )

    def test_count_thai_matches_python(self) -> None:
        from pythainlp.util.thai import _py_count_thai as py_count_thai

        test_cases = [
            ("ไทยเอ็นแอลพี 3.0", ""),
            ("PyThaiNLP 3.0", ""),
            ("ใช้งาน PyThaiNLP 3.0", ""),
            ("", ""),
            ("กขค", ""),
            ("กขค 123", " 0123456789"),
        ]
        for text, ignore in test_cases:
            with self.subTest(text=repr(text)):
                self.assertAlmostEqual(
                    fast_count_thai(text, ignore),
                    py_count_thai(text, ignore),
                    places=6,
                    msg=f"Mismatch for {repr(text)!r}",
                )


class FastNormalizeCorrectnessTest(unittest.TestCase):
    """Verify Cython _normalize_fast functions match Python implementations."""

    def setUp(self) -> None:
        if not HAVE_EXT:
            self.skipTest(
                "pythainlp._ext Cython extensions not built; skipping"
            )

    def test_remove_tonemark_matches_python(self) -> None:
        from pythainlp.util.normalize import (
            _py_remove_tonemark as py_remove_tonemark,
        )

        test_cases = [
            "จิ้น",
            "เก๋า",
            "สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด",
            "",
            "no tonemarks here ก ข ค",
            "ก่ก้ก๊ก๋",
            "mixed Thai and English text กับ tone marks ่้๊๋",
        ]
        for text in test_cases:
            with self.subTest(text=repr(text)):
                self.assertEqual(
                    fast_remove_tonemark(text),
                    py_remove_tonemark(text),
                    f"Mismatch for {repr(text)}",
                )

    def test_remove_tonemark_removes_all_four(self) -> None:
        # Each of the four Thai tone marks must be removed
        from pythainlp import thai_tonemarks

        for mark in thai_tonemarks:
            text = f"ก{mark}า"
            result = fast_remove_tonemark(text)
            self.assertNotIn(
                mark,
                result,
                f"Tone mark U+{ord(mark):04X} was not removed",
            )

    def test_remove_dup_spaces_matches_python(self) -> None:
        from pythainlp.util.normalize import (
            remove_dup_spaces as py_remove_dup_spaces,
        )

        test_cases = [
            "ก    ข    ค",
            "  ab  c d  ",
            "normal spaces",
            "",
            "   leading",
            "trailing   ",
            "a  b  c",
        ]
        for text in test_cases:
            with self.subTest(text=repr(text)):
                self.assertEqual(
                    fast_remove_dup_spaces(text),
                    py_remove_dup_spaces(text),
                    f"Mismatch for {repr(text)}",
                )

    def test_remove_dup_spaces_preserves_tabs(self) -> None:
        # Tabs are NOT collapsed (only ASCII 0x20 spaces are)
        from pythainlp.util.normalize import (
            remove_dup_spaces as py_remove_dup_spaces,
        )

        text = "a\t\tb"
        self.assertEqual(
            fast_remove_dup_spaces(text), py_remove_dup_spaces(text)
        )

