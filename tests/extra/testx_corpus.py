# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch

from nltk.corpus import wordnet as wn

from pythainlp.corpus import wordnet
from pythainlp.corpus.wordnet import _ensure_corpus, _omw_package


class CorpusTestCaseX(unittest.TestCase):
    def test_wordnet(self):
        self.assertIsNotNone(wordnet.langs())
        self.assertIn("tha", wordnet.langs())

        self.assertEqual(
            wordnet.synset("spy.n.01").lemma_names("tha"), ["สปาย", "สายลับ"]
        )
        self.assertIsNotNone(wordnet.synsets("นก"))
        self.assertIsNotNone(wordnet.all_synsets(pos=wn.ADJ))

        self.assertIsNotNone(wordnet.lemmas("นก"))
        self.assertIsNotNone(wordnet.all_lemma_names(pos=wn.ADV))
        self.assertIsNotNone(wordnet.lemma("cat.n.01.cat"))

        self.assertEqual(wordnet.morphy("dogs"), "dog")
        # morphy with pos=None (default) and with explicit pos
        self.assertEqual(wordnet.morphy("dogs", pos=None), "dog")
        self.assertEqual(wordnet.morphy("dogs", pos="n"), "dog")

        bird = wordnet.synset("bird.n.01")
        mouse = wordnet.synset("mouse.n.01")
        self.assertEqual(
            wordnet.path_similarity(bird, mouse), bird.path_similarity(mouse)
        )
        self.assertEqual(
            wordnet.wup_similarity(bird, mouse), bird.wup_similarity(mouse)
        )
        self.assertEqual(
            wordnet.lch_similarity(bird, mouse), bird.lch_similarity(mouse)
        )

        cat_key = wordnet.synsets("แมว")[0].lemmas()[0].key()
        self.assertIsNotNone(wordnet.lemma_from_key(cat_key))


class WordNetDataTestCaseX(unittest.TestCase):
    """Tests for choosing and installing NLTK WordNet data, offline."""

    def test_omw_package(self):
        cases = {
            "3.10.3": "omw-2.0",
            "3.10": "omw-2.0",
            "3.10.0rc1": "omw-2.0",
            "4.0.0": "omw-2.0",
            "3.9.2": "omw-1.4",
            "3.9.0rc1": "omw-1.4",
            "3.6.6": "omw-1.4",
            "3.6.5": "omw",
            "3.3": "omw",
            "unknown": "omw-2.0",
        }
        for version, expected in cases.items():
            with self.subTest(version=version):
                self.assertEqual(_omw_package(version), expected)

    @patch("nltk.download")
    @patch("nltk.data.find", return_value="path")
    def test_ensure_corpus_found_unzipped(self, find, download):
        _ensure_corpus("omw-2.0")
        find.assert_called_once_with("corpora/omw-2.0")
        download.assert_not_called()

    @patch("nltk.download")
    @patch("nltk.data.find", side_effect=[LookupError, "path"])
    def test_ensure_corpus_found_zip(self, find, download):
        _ensure_corpus("omw-2.0")
        self.assertEqual(find.call_count, 2)
        find.assert_called_with("corpora/omw-2.0.zip")
        download.assert_not_called()

    @patch("nltk.download")
    @patch("nltk.data.find", side_effect=LookupError)
    def test_ensure_corpus_missing(self, find, download):
        _ensure_corpus("omw-2.0")
        self.assertEqual(find.call_count, 2)
        download.assert_called_once_with("omw-2.0")
