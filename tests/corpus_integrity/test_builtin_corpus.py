# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Test integrity and parseability of built-in corpus files.

These tests verify that all corpus files included in the package
can be loaded and parsed correctly.
"""

import unittest

from pythainlp.corpus import (
    countries,
    find_synonyms,
    get_corpus,
    provinces,
    thai_family_names,
    thai_female_names,
    thai_icu_words,
    thai_male_names,
    thai_negations,
    thai_orst_words,
    thai_stopwords,
    thai_syllables,
    thai_synonyms,
    thai_volubilis_words,
    thai_wikipedia_titles,
    thai_words,
    ttc,
)


class BuiltinCorpusIntegrityTestCase(unittest.TestCase):
    """Test integrity of built-in corpus files."""

    def test_negations(self):
        """Test thai_negations corpus can be loaded and is not empty."""
        result = thai_negations()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        # Verify it contains actual Thai content
        self.assertTrue(any('\u0e00' <= char <= '\u0e7f' for item in result for char in item))

    def test_stopwords(self):
        """Test thai_stopwords corpus can be loaded and is not empty."""
        result = thai_stopwords()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        # Verify it contains actual Thai content
        self.assertTrue(any('\u0e00' <= char <= '\u0e7f' for item in result for char in item))

    def test_syllables(self):
        """Test thai_syllables corpus can be loaded and is not empty."""
        result = thai_syllables()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        # Verify it contains actual Thai content
        self.assertTrue(any('\u0e00' <= char <= '\u0e7f' for item in result for char in item))

    def test_words(self):
        """Test thai_words corpus can be loaded and is not empty."""
        result = thai_words()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        # Verify it contains actual Thai content
        self.assertTrue(any('\u0e00' <= char <= '\u0e7f' for item in result for char in item))

    def test_synonyms(self):
        """Test thai_synonyms corpus can be loaded and parsed correctly."""
        result = thai_synonyms()
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        # Test that find_synonyms works with the loaded data
        synonyms = find_synonyms("หมู")
        self.assertIsInstance(synonyms, list)
        self.assertGreater(len(synonyms), 0)

    def test_icu_words(self):
        """Test thai_icu_words corpus can be loaded and is not empty."""
        result = thai_icu_words()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_orst_words(self):
        """Test thai_orst_words corpus can be loaded and is not empty."""
        result = thai_orst_words()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_volubilis_words(self):
        """Test thai_volubilis_words corpus can be loaded and is not empty."""
        result = thai_volubilis_words()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_wikipedia_titles(self):
        """Test thai_wikipedia_titles corpus can be loaded and is not empty."""
        result = thai_wikipedia_titles()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_countries(self):
        """Test countries corpus can be loaded and is not empty."""
        result = countries()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_provinces(self):
        """Test provinces corpus can be loaded and parsed correctly."""
        result = provinces()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        
        # Test with details
        result_details = provinces(details=True)
        self.assertIsInstance(result_details, list)
        self.assertEqual(len(result), len(result_details))

    def test_family_names(self):
        """Test thai_family_names corpus can be loaded and is not empty."""
        result = thai_family_names()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_female_names(self):
        """Test thai_female_names corpus can be loaded and is not empty."""
        result = thai_female_names()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_male_names(self):
        """Test thai_male_names corpus can be loaded and is not empty."""
        result = thai_male_names()
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)

    def test_ttc_freq(self):
        """Test TTC frequency corpus can be loaded and parsed correctly."""
        result = ttc.word_freqs()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        # Verify format: list of (word, frequency) tuples
        for item in result[:10]:  # Check first 10 items
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)
        
        # Test unigram version
        result_unigram = ttc.unigram_word_freqs()
        self.assertIsInstance(result_unigram, dict)
        self.assertGreater(len(result_unigram), 0)

    def test_tnc_freq(self):
        """Test TNC frequency corpus can be loaded and parsed correctly."""
        # Test unigram from built-in file
        result = get_corpus("tnc_freq.txt")
        self.assertIsInstance(result, frozenset)
        self.assertGreater(len(result), 0)
        # Verify format: tab-separated word and frequency
        for line in list(result)[:10]:  # Check first 10 lines
            parts = line.split('\t')
            self.assertGreaterEqual(len(parts), 2)
