# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import os
import unittest

import nltk
from nltk.corpus import wordnet as wn
from requests import Response

from pythainlp.corpus import (
    conceptnet,
    countries,
    download,
    find_synonyms,
    get_corpus_db,
    get_corpus_db_detail,
    get_corpus_default_db,
    get_corpus_path,
    oscar,
    provinces,
    remove,
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
    tnc,
    ttc,
    wordnet,
)
from pythainlp.corpus.util import revise_newmm_default_wordset


class TestCorpusPackage(unittest.TestCase):
    def test_conceptnet(self):
        self.assertIsNotNone(conceptnet.edges("รัก"))

    def test_corpus(self):
        self.assertIsInstance(thai_negations(), frozenset)
        self.assertGreater(len(thai_negations()), 0)
        self.assertIsInstance(thai_stopwords(), frozenset)
        self.assertGreater(len(thai_stopwords()), 0)
        self.assertIsInstance(thai_syllables(), frozenset)
        self.assertGreater(len(thai_syllables()), 0)
        self.assertIsInstance(thai_synonyms(), dict)
        self.assertGreater(len(thai_synonyms()), 0)

        self.assertIsInstance(thai_icu_words(), frozenset)
        self.assertGreater(len(thai_icu_words()), 0)
        self.assertIsInstance(thai_orst_words(), frozenset)
        self.assertGreater(len(thai_orst_words()), 0)
        self.assertIsInstance(thai_volubilis_words(), frozenset)
        self.assertGreater(len(thai_volubilis_words()), 0)
        self.assertIsInstance(thai_wikipedia_titles(), frozenset)
        self.assertGreater(len(thai_wikipedia_titles()), 0)
        self.assertIsInstance(thai_words(), frozenset)
        self.assertGreater(len(thai_words()), 0)

        self.assertIsInstance(countries(), frozenset)
        self.assertGreater(len(countries()), 0)
        self.assertIsInstance(provinces(), frozenset)
        self.assertGreater(len(provinces()), 0)
        self.assertIsInstance(provinces(details=True), list)
        self.assertEqual(
            len(provinces(details=False)), len(provinces(details=True))
        )

        self.assertIsInstance(thai_family_names(), frozenset)
        self.assertIsInstance(list(thai_family_names())[0], str)
        self.assertIsInstance(thai_female_names(), frozenset)
        self.assertIsInstance(thai_male_names(), frozenset)

        self.assertIsNotNone(get_corpus_default_db("thainer", "1.5.1"))
        self.assertIsNotNone(get_corpus_default_db("thainer"))
        self.assertIsNone(get_corpus_default_db("thainer", "1.2"))

        # BEGIN - Test non-exists
        self.assertIsInstance(
            get_corpus_db("https://example.com/XXXXXX0lkjasd/SXfmskdjKKXXX"),
            Response,
        )  # URL does not exist, should get 404 response
        self.assertIsNone(get_corpus_db("XXXlkja3sfdXX"))  # Invalid URL
        self.assertEqual(
            get_corpus_db_detail("XXXmx3KSXX"), {}
        )  # corpus does not exist
        self.assertEqual(
            get_corpus_db_detail("XXXmx3KSXX", version="0.2"), {}
        )  # corpus does not exist
        self.assertIsNone(get_corpus_path("XXXkdjfBzc"))  # query non-existing
        self.assertFalse(
            download(name="test", url="wrongurl00AAfcX2df")
        )  # URL not exist
        self.assertFalse(
            download(name="XxxXXxxx817d37sf")
        )  # corpus name not exist
        # END - Test non-exists

        # BEGIN - Test download
        self.assertTrue(download("test"))  # download the first time
        self.assertTrue(download(name="test", force=True))  # force download
        self.assertTrue(download(name="test"))  # try download existing
        self.assertIsNotNone(get_corpus_db_detail("test"))  # corpus exists
        self.assertIsNotNone(get_corpus_path("test"))  # corpus exists
        self.assertIsNone(get_corpus_default_db("test"))
        self.assertTrue(remove("test"))  # remove existing
        self.assertFalse(remove("test"))  # remove non-existing
        # END - Test download

        # TODO: Need this clean up this "test" download test
        # BEGIN - Need to clean up this section
        self.assertFalse(download(name="test", version="0.0"))
        self.assertFalse(download(name="test", version="0.0.0"))
        self.assertFalse(download(name="test", version="0.0.1"))
        self.assertFalse(download(name="test", version="0.0.2"))
        self.assertFalse(download(name="test", version="0.0.3"))
        self.assertFalse(download(name="test", version="0.0.4"))
        self.assertIsNotNone(download(name="test", version="0.0.5"))
        self.assertTrue(download("test"))
        self.assertIsNotNone(remove("test"))  # remove existing
        self.assertIsNotNone(download(name="test", version="0.0.6"))
        self.assertIsNotNone(download(name="test", version="0.0.7"))
        self.assertIsNotNone(download(name="test", version="0.0.8"))
        self.assertIsNotNone(download(name="test", version="0.0.9"))
        self.assertIsNotNone(download(name="test", version="0.0.10"))
        with self.assertRaises(Exception) as context:
            # Force re-downloading since the corpus already exists
            self.assertIsNotNone(download(
                name="test", version="0.0.11", force=True
            ))
        self.assertTrue(
            "Hash does not match expected."
            in
            str(context.exception)
        )
        self.assertIsNotNone(download(name="test", version="0.1"))
        self.assertIsNotNone(remove("test"))
        # END - Need to clean up this section

    def test_oscar(self):
        self.assertIsNotNone(oscar.word_freqs())
        self.assertIsNotNone(oscar.unigram_word_freqs())

    def test_tnc(self):
        self.assertIsNotNone(tnc.word_freqs())
        self.assertIsNotNone(tnc.unigram_word_freqs())
        self.assertIsNotNone(tnc.bigram_word_freqs())
        self.assertIsNotNone(tnc.trigram_word_freqs())

    def test_ttc(self):
        self.assertIsNotNone(ttc.word_freqs())
        self.assertIsNotNone(ttc.unigram_word_freqs())

    def test_wordnet(self):
        nltk.download('omw-1.4', force=True)  # load wordnet
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

    def test_revise_wordset(self):
        training_data = [
            ["ถวิล อุดล", " ", "เป็น", "นักการเมือง", "หนึ่ง", "ใน"],
            ["สี่เสืออีสาน", " ", "ซึ่ง", "ประกอบ", "ด้วย", "ตัว", "นายถวิล"],
            ["เอง", " ", "นายทองอินทร์ ภูริพัฒน์", " ", "นายเตียง ศิริขันธ์"],
            [" ", "และ", "นายจำลอง ดาวเรือง", " ", "และ", "เป็น", "รัฐมนตรี"],
            ["ที่", "ถูก", "สังหาร", "เมื่อ", "ปี", " ", "พ.ศ.", " ", "2492"],
        ]
        self.assertIsInstance(revise_newmm_default_wordset(training_data), set)

    def test_zip(self):
        p = get_corpus_path("test_zip")
        self.assertEqual(os.path.isdir(p), True)
        self.assertEqual(remove("test_zip"), True)

    def test_find_synonyms(self):
        self.assertEqual(
            find_synonyms("หมู"),
            ['จรุก', 'วราหะ', 'วราห์', 'ศูกร', 'สุกร']
        )
        self.assertEqual(find_synonyms("1"), [])
