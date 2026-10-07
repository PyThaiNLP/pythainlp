# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.lm import calculate_ngram_counts, remove_repeated_ngrams


class LMTestCase(unittest.TestCase):
    def test_calculate_ngram_counts(self):
        self.assertEqual(
            calculate_ngram_counts(["1", "2", "3", "4"]),
            {
                ("1", "2"): 1,
                ("2", "3"): 1,
                ("3", "4"): 1,
                ("1", "2", "3"): 1,
                ("2", "3", "4"): 1,
                ("1", "2", "3", "4"): 1,
            },
        )

    def test_remove_repeated_ngrams(self):
        texts = ["เอา", "เอา", "แบบ", "แบบ", "แบบ", "ไหน"]
        self.assertEqual(
            remove_repeated_ngrams(texts, n=1), ["เอา", "แบบ", "ไหน"]
        )
        self.assertEqual(
            remove_repeated_ngrams(texts, n=2),
            ["เอา", "เอา", "แบบ", "แบบ", "ไหน"],
        )

    def test_lm_phayathaibert_segment_empty(self):
        from pythainlp.lm.phayathaibert import segment
        self.assertEqual(segment(""), [])
        self.assertEqual(segment(None), [])  # type: ignore[arg-type]

    def test_lm_wangchanberta_segment_empty(self):
        from pythainlp.lm.wangchanberta import segment
        self.assertEqual(segment(""), [])
        self.assertEqual(segment(None), [])  # type: ignore[arg-type]

    def test_lm_wangchanberta_fix_span_error(self):
        from pythainlp.lm.wangchanberta.core import NamedEntityRecognition

        class Tokenizer:
            def decode(self, token: int) -> str:
                return {1: " ", 2: "word", 3: "<s>"}[token]

        tagger = object.__new__(NamedEntityRecognition)
        tagger.tokenizer = Tokenizer()
        self.assertEqual(
            tagger._fix_span_error([1, 2, 3], ["B-PER", "B-PER", "O"]),
            [(" ", "O"), ("word", "B-PER")],
        )

    def test_deprecated_phayathaibert(self):
        import importlib
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import pythainlp.phayathaibert
            importlib.reload(pythainlp.phayathaibert)
        self.assertTrue(
            any(issubclass(warning.category, DeprecationWarning) for warning in w)
        )

    def test_deprecated_wangchanberta(self):
        import importlib
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import pythainlp.wangchanberta
            importlib.reload(pythainlp.wangchanberta)
        self.assertTrue(
            any(issubclass(warning.category, DeprecationWarning) for warning in w)
        )
