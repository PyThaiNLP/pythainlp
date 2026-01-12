# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

import nltk
from nltk.corpus import wordnet as wn

from pythainlp.corpus import wordnet


class CorpusTestCaseX(unittest.TestCase):
    def test_wordnet(self):
        nltk.download("omw-1.4", force=True)  # load wordnet
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
