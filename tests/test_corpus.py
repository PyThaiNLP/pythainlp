# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from nltk.corpus import wordnet as wn

from pythainlp.corpus import (
    _CORPUS_PATH,
    conceptnet,
    countries,
    download,
    provinces,
    remove,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
    tnc,
    ttc,
    wordnet,
    thai_female_names,
    thai_male_names,
    get_corpus_db_detail
)
from pythainlp.corpus.common import _THAI_WORDS_FILENAME


class TestCorpusPackage(unittest.TestCase):

    def test_conceptnet(self):
        self.assertIsNotNone(conceptnet.edges("รัก"))

    def test_corpus(self):
        self.assertIsNotNone(countries())
        self.assertIsNotNone(provinces())
        self.assertIsNotNone(thai_negations())
        self.assertIsNotNone(thai_stopwords())
        self.assertIsNotNone(thai_syllables())
        self.assertIsNotNone(thai_words())
        self.assertIsNone(download("test"))
        self.assertIsNone(download("test",force=True))
        self.assertIsNotNone(get_corpus_db_detail("test"))
        self.assertIsNotNone(remove("test"))
        self.assertIsNotNone(thai_female_names())
        self.assertIsNotNone(thai_male_names())

    def test_tnc(self):
        self.assertIsNotNone(tnc.word_freqs())
        self.assertIsNotNone(tnc.word_freq("นก"))

    def test_ttc(self):
        self.assertIsNotNone(ttc.word_freqs())

    def test_wordnet(self):
        self.assertIsNotNone(wordnet.langs())

        self.assertEqual(
            wordnet.synset("spy.n.01").lemma_names("tha"), ["สปาย", "สายลับ"]
        )
        self.assertIsNotNone(wordnet.synsets("นก"))
        self.assertIsNotNone(wordnet.all_synsets(pos=wn.ADJ))

        self.assertIsNotNone(wordnet.lemmas("นก"))
        self.assertIsNotNone(wordnet.all_lemma_names(pos=wn.ADV))
        self.assertIsNotNone(wordnet.lemma("cat.n.01.cat"))

        self.assertEqual(wordnet.morphy("dogs"), "dog")

        bird = wordnet.synset("bird.n.01")
        mouse = wordnet.synset("mouse.n.01")
        self.assertEqual(
            wordnet.path_similarity(bird, mouse), bird.path_similarity(mouse)
        )
        self.assertEqual(
            wordnet.wup_similarity(bird, mouse), bird.wup_similarity(mouse)
        )

        cat_key = wordnet.synsets("แมว")[0].lemmas()[0].key()
        self.assertIsNotNone(wordnet.lemma_from_key(cat_key))
