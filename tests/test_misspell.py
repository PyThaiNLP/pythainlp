# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
import numpy as np
from pythainlp.tools.misspell import misspell


def _count_difference(st1, st2):
    # this assumes len(st1) == len(st2)

    count = 0
    for i in range(len(st1)):
        if st1[i] != st2[i]:
            count += 1

    return count


class TestTextMisspellPackage(unittest.TestCase):
    def setUp(self):
        self.texts = ["เรารักคุณมากที่สุดในโลก", "เราอยู่ที่มหาวิทยาลัยขอนแก่น"]

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
