# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from typing import cast

import numpy as np

from pythainlp.tools.misspell import (
    find_misspell_candidates,
    misspell,
    search_location_of_character,
)


def _count_difference(st1: str, st2: str) -> int:
    # this assumes len(st1) == len(st2)

    count = 0
    for i, c in enumerate(st1):
        if c != st2[i]:
            count += 1

    return count


class MisspellTestCaseC(unittest.TestCase):
    def setUp(self):
        self.texts = ["เรารักคุณมากที่สุดในโลก", "เราอยู่ที่มหาวิทยาลัยขอนแก่น"]

    def test_misspell_edge_cases(self):
        # Edge case: empty string
        self.assertEqual(misspell(""), "")
        # Edge case: single character with ratio 0
        self.assertEqual(misspell("ก", ratio=0), "ก")
        # Edge case: single character with ratio 1
        result = misspell("ก", ratio=1)
        self.assertEqual(len(result), 1)
        # Edge case: None raises TypeError
        with self.assertRaises(TypeError):
            misspell(None)  # type: ignore[arg-type]

    def test_misspell_naive(self):
        for text in self.texts:
            misspelled = misspell(text, ratio=0.1)

            self.assertEqual(len(text), len(misspelled))

            diff = _count_difference(text, misspelled)

            self.assertGreater(diff, 0, "we have some misspells.")

    def test_misspell_with_ratio_0_percent(self):
        for text in self.texts:
            misspelled = misspell(text, ratio=0.0)

            self.assertEqual(len(text), len(misspelled))

            diff = _count_difference(text, misspelled)

            self.assertEqual(
                diff, 0, "we shouldn't have any misspell with ratio=0."
            )

    def test_misspell_with_ratio_50_percent(self):
        for text in self.texts:
            misspelled = misspell(text, ratio=0.5)

            self.assertEqual(len(text), len(misspelled))

            diff = _count_difference(text, misspelled)

            self.assertLessEqual(
                np.abs(diff - 0.5 * len(text)),
                2,
                f"expect 0.5*len(text)±2 misspells with ratio=0.5. (Δ={diff})",
            )

    def test_misspell_with_ratio_100_percent(self):
        for text in self.texts:
            misspelled = misspell(text, ratio=1)

            self.assertEqual(len(text), len(misspelled))

            diff = _count_difference(text, misspelled)

            self.assertLessEqual(
                np.abs(diff - len(text)),
                2,
                f"expect len(text)-2 misspells with ratio=1.5. (Δ={diff})",
            )

    def test_search_location_of_character(self):
        """Test search_location_of_character function."""
        # Test Thai characters
        loc = search_location_of_character("ก")
        self.assertIsNotNone(loc)
        # loc shape is (language_ix, is_shift, row, pos)
        self.assertEqual(len(loc), 4)  # type: ignore[arg-type]

        # Test English characters
        loc = search_location_of_character("a")
        self.assertIsNotNone(loc)
        # loc shape is (language_ix, is_shift, row, pos)
        self.assertEqual(len(loc), 4)  # type: ignore[arg-type]

        # Test shifted characters
        loc = search_location_of_character("A")
        self.assertIsNotNone(loc)

        # Test numbers
        loc = search_location_of_character("1")
        self.assertIsNotNone(loc)

        # Test character not in keyboard
        loc = search_location_of_character("€")
        self.assertIsNone(loc)

        # Test empty string
        # Note: Empty string returns a location because Python's "in" operator
        # matches empty string at the beginning of any string
        loc = search_location_of_character("")
        self.assertIsNotNone(loc)

    def test_find_misspell_candidates(self):
        """Test find_misspell_candidates function."""
        # Test Thai character
        candidates = find_misspell_candidates("ก")
        self.assertIsNotNone(candidates)
        self.assertIsInstance(candidates, list)
        candidates = cast("list[str]", candidates)  # for type checker
        self.assertGreater(len(candidates), 0)

        # Test English character
        candidates = find_misspell_candidates("a")
        self.assertIsNotNone(candidates)
        self.assertIsInstance(candidates, list)
        candidates = cast("list[str]", candidates)  # for type checker
        self.assertGreater(len(candidates), 0)

        # Test character not in keyboard
        candidates = find_misspell_candidates("€")
        self.assertIsNone(candidates)

        # Test that candidates are different from input
        candidates = find_misspell_candidates("ด")
        if candidates:
            for candidate in candidates:
                # Candidates should be strings
                self.assertIsInstance(candidate, str)
