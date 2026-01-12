# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.lm import calculate_ngram_counts, remove_repeated_ngrams


class LMTestCase(unittest.TestCase):
    def test_calculate_ngram_counts(self):
        self.assertEqual(
            calculate_ngram_counts(['1', '2', '3', '4']),
            {
                ('1', '2'): 1,
                ('2', '3'): 1,
                ('3', '4'): 1,
                ('1', '2', '3'): 1,
                ('2', '3', '4'): 1,
                ('1', '2', '3', '4'): 1
            }
        )

    def test_remove_repeated_ngrams(self):
        texts = ['เอา', 'เอา', 'แบบ', 'แบบ', 'แบบ', 'ไหน']
        self.assertEqual(
            remove_repeated_ngrams(texts, n=1),
            ['เอา', 'แบบ', 'ไหน']
        )
        self.assertEqual(
            remove_repeated_ngrams(texts, n=2),
            ['เอา', 'เอา', 'แบบ', 'แบบ', 'ไหน']
        )
