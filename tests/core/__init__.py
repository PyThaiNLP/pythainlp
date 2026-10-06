# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Unit test.

Each file in tests/ is for each main package.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.core.test_ancient",
    "tests.core.test_augment_wordnet",
    "tests.core.test_benchmarks_error_rate",
    "tests.core.test_benchmarks_metrics",
    "tests.core.test_braille",
    "tests.core.test_cli",
    "tests.core.test_cli_benchmark",
    "tests.core.test_branches_offline",
    "tests.core.test_corpus",
    "tests.core.test_corpus_core_internals",
    "tests.core.test_fastthaig2p",
    "tests.core.test_generate",
    "tests.core.test_generate_bigram",
    "tests.core.test_generate_core",
    "tests.core.test_khavee",
    "tests.core.test_khavee_chars",
    "tests.core.test_lm_text_util",
    "tests.core.test_morpheme",
    "tests.core.test_morpheme_word_formation",
    "tests.core.test_phayathaibert_preprocess",
    "tests.core.test_security",
    "tests.core.test_soundex",
    "tests.core.test_soundex_engines",
    "tests.core.test_spell",
    "tests.core.test_summarize_offline",
    "tests.core.test_tag",
    "tests.core.test_tokenize",
    "tests.core.test_tokenize_core",
    "tests.core.test_tokenize_han_solo",
    "tests.core.test_tokenize_longest",
    "tests.core.test_tokenize_multi_cut",
    "tests.core.test_tokenize_nercut",
    "tests.core.test_tokenize_newmm_internals",
    "tests.core.test_tokenize_thaisumcut",
    "tests.core.test_tools",
    "tests.core.test_transliterate",
    "tests.core.test_transliterate_royin",
    "tests.core.test_transliterate_spoonerism",
    "tests.core.test_transliterate_wiktionary",
    "tests.core.test_transliterate_wiktionary_chars",
    "tests.core.test_transliterate_wunsen",
    "tests.core.test_util",
    "tests.core.test_util_date_strptime",
    "tests.core.test_util_normalize_lcs",
    "tests.core.test_util_numtoword",
    "tests.core.test_util_strftime",
    "tests.core.test_util_syllable",
    "tests.core.test_util_thai",
    "tests.core.test_util_thai_lunar_date",
    "tests.core.test_util_time",
]


def load_tests(
    loader: TestLoader, standard_tests: TestSuite, pattern: str
) -> TestSuite:
    """
    Load the test modules listed in ``test_packages``.

    See: https://docs.python.org/3/library/unittest.html#id1
    """
    suite = TestSuite()
    for test_package in test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)
    return suite


if __name__ == "__main__":
    import unittest

    unittest.main()
