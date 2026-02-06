# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Test integrity and parseability of downloadable corpus files.

These tests verify that corpus files that need to be downloaded
can be fetched and parsed correctly. These tests may take longer
to run due to network downloads.
"""

import unittest

from pythainlp.corpus import oscar, tnc


class DownloadableCorpusIntegrityTestCase(unittest.TestCase):
    """Test integrity of downloadable corpus files."""

    def test_oscar_corpus(self):
        """Test OSCAR corpus can be downloaded and parsed correctly."""
        # Test word_freqs
        result = oscar.word_freqs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Verify format: list of (word, frequency) tuples
        for item in result[:10]:  # Check first 10 items
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)
            self.assertGreater(item[1], 0)
        
        # Test unigram_word_freqs
        result_unigram = oscar.unigram_word_freqs()
        self.assertIsNotNone(result_unigram)
        self.assertIsInstance(result_unigram, dict)
        self.assertGreater(len(result_unigram), 0)
        
        # Verify dict values are integers
        for word, freq in list(result_unigram.items())[:10]:
            self.assertIsInstance(word, str)
            self.assertIsInstance(freq, int)
            self.assertGreater(freq, 0)

    def test_tnc_unigram(self):
        """Test TNC unigram corpus can be loaded and parsed correctly."""
        result = tnc.word_freqs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Verify format
        for item in result[:10]:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)
        
        # Test unigram version
        result_unigram = tnc.unigram_word_freqs()
        self.assertIsNotNone(result_unigram)
        self.assertIsInstance(result_unigram, dict)
        self.assertGreater(len(result_unigram), 0)

    def test_tnc_bigram(self):
        """Test TNC bigram corpus can be downloaded and parsed correctly."""
        result = tnc.bigram_word_freqs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        
        # Verify format: dict with tuple keys (word1, word2) -> frequency
        for key, freq in list(result.items())[:10]:
            self.assertIsInstance(key, tuple)
            self.assertEqual(len(key), 2)
            self.assertIsInstance(key[0], str)
            self.assertIsInstance(key[1], str)
            self.assertIsInstance(freq, int)
            self.assertGreater(freq, 0)

    def test_tnc_trigram(self):
        """Test TNC trigram corpus can be downloaded and parsed correctly."""
        result = tnc.trigram_word_freqs()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        
        # Verify format: dict with tuple keys (word1, word2, word3) -> frequency
        for key, freq in list(result.items())[:10]:
            self.assertIsInstance(key, tuple)
            self.assertEqual(len(key), 3)
            self.assertIsInstance(key[0], str)
            self.assertIsInstance(key[1], str)
            self.assertIsInstance(key[2], str)
            self.assertIsInstance(freq, int)
            self.assertGreater(freq, 0)
