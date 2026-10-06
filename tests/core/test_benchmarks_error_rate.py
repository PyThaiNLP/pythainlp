# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for the edit-distance and LCS helpers.

The helpers are in pythainlp.benchmarks.metrics.

Golden cases were recorded from the code before the shared-helper refactor.
Word tokenization is replaced with a whitespace split.
"""

from __future__ import annotations

import math
import unittest
from unittest import mock

from pythainlp.benchmarks import character_error_rate, word_error_rate
from pythainlp.benchmarks.metrics import _error_rate, _lcs_length

# (reference, hypothesis, expected error rate)
CER_CASES: list[tuple[str, str, float]] = [
    ("", "", 0.0),
    ("", "ab", math.inf),
    ("ab", "", 1.0),
    ("ab", "ab", 0.0),
    ("abc", "axc", 0.3333333333333333),
    ("abc", "ab", 0.3333333333333333),
    ("ab", "abcd", 1.0),
    ("kitten", "sitting", 0.5),
    ("สวัสดี", "สวัสดีครับ", 0.6666666666666666),
    ("a b c", "a c", 0.4),
    ("a b", "x y z", 1.3333333333333333),
    ("a", "cb", 2.0),
    ("c b b c a c", "b", 0.9090909090909091),
    ("c b c c", " caac ", 0.7142857142857143),
    ("b b c", "bbb", 0.6),
    ("a", "bbcb  ", 6.0),
    ("c b c b b b", "  b", 0.7272727272727273),
]
WER_CASES: list[tuple[str, str, float]] = [
    ("", "", 0.0),
    ("", "ab", math.inf),
    ("ab", "", 1.0),
    ("ab", "ab", 0.0),
    ("abc", "axc", 1.0),
    ("abc", "ab", 1.0),
    ("ab", "abcd", 1.0),
    ("kitten", "sitting", 1.0),
    ("สวัสดี", "สวัสดีครับ", 1.0),
    ("a b c", "a c", 0.3333333333333333),
    ("a b", "x y z", 1.5),
    ("a", "cb", 1.0),
    ("c b b c a c", "b", 0.8333333333333334),
    ("c b c c", " caac ", 1.0),
    ("b b c", "bbb", 1.0),
    ("a", "bbcb  ", 1.0),
    ("c b c b b b", "  b", 0.8333333333333334),
]
# (first sequence, second sequence, expected LCS length)
LCS_CASES: list[tuple[list[str], list[str], int]] = [
    ([], [], 0),
    (["a"], [], 0),
    (["a", "b", "c", "b", "d", "a", "b"], ["b", "d", "c", "a", "b", "a"], 4),
    (["a", "b", "c"], ["a", "b", "c"], 3),
    (["a", "b", "c"], ["x", "y", "z"], 0),
    (["สวัสดี", "ครับ"], ["ครับ"], 1),
]


def _split(
    text: str, engine: str = "newmm", keep_whitespace: bool = True
) -> list[str]:
    return text.split()


class ErrorRateTestCase(unittest.TestCase):
    def test_character_error_rate(self) -> None:
        for ref, hyp, expected in CER_CASES:
            with self.subTest(ref=ref, hyp=hyp):
                self.assertEqual(character_error_rate(ref, hyp), expected)

    def test_word_error_rate(self) -> None:
        with mock.patch("pythainlp.tokenize.word_tokenize", _split):
            for ref, hyp, expected in WER_CASES:
                with self.subTest(ref=ref, hyp=hyp):
                    self.assertEqual(word_error_rate(ref, hyp), expected)

    def test_error_rate_accepts_any_sequence_of_strings(self) -> None:
        self.assertEqual(_error_rate(["a", "b"], ["a"]), 0.5)
        self.assertEqual(_error_rate("ab", "a"), 0.5)
        self.assertEqual(_error_rate([], []), 0.0)
        self.assertEqual(_error_rate([], ["a"]), math.inf)

    def test_character_error_rate_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            character_error_rate(None, "a")  # type: ignore[arg-type]


class LcsLengthTestCase(unittest.TestCase):
    def test_golden_cases(self) -> None:
        for x, y, expected in LCS_CASES:
            with self.subTest(x=x, y=y):
                self.assertEqual(_lcs_length(x, y), expected)

    def test_wrong_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            _lcs_length(None, ["a"])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
