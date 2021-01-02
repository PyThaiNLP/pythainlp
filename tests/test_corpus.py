# -*- coding: utf-8 -*-

import unittest

from nltk.corpus import wordnet as wn
from pythainlp.corpus import (
    conceptnet,
    countries,
    download,
    get_corpus_db,
    get_corpus_db_detail,
    get_corpus_path,
    provinces,
    remove,
    thai_family_names,
    thai_female_names,
    thai_male_names,
    thai_negations,
    thai_stopwords,
    thai_syllables,
    thai_words,
    tnc,
    ttc,
    wordnet,
)
from pythainlp.corpus.util import revise_newmm_default_wordset
from requests import Response


class TestCorpusPackage(unittest.TestCase):
    def test_conceptnet(self):
        self.assertIsNotNone(conceptnet.edges("รัก"))

    def test_corpus(self):
        self.assertIsInstance(thai_negations(), frozenset)
        self.assertIsInstance(thai_stopwords(), frozenset)
        self.assertIsInstance(thai_syllables(), frozenset)
        self.assertIsInstance(thai_words(), frozenset)

        self.assertIsInstance(countries(), frozenset)
        self.assertIsInstance(provinces(), frozenset)
        self.assertIsInstance(provinces(details=True), list)
        self.assertEqual(
            len(provinces(details=False)), len(provinces(details=True))
        )
        self.assertIsInstance(thai_family_names(), frozenset)
        self.assertIsInstance(list(thai_family_names())[0], str)
        self.assertIsInstance(thai_female_names(), frozenset)
        self.assertIsInstance(thai_male_names(), frozenset)

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

        self.assertTrue(download("test"))  # download the first time
        self.assertTrue(download(name="test", force=True))  # force download
        self.assertTrue(download(name="test"))  # try download existing
        self.assertFalse(
            download(name="test", url="wrongurl")
        )  # URL not exist
        self.assertFalse(
            download(name="XxxXXxxx817d37sf")
        )  # corpus name not exist
        self.assertIsNotNone(get_corpus_db_detail("test"))  # corpus exists
        self.assertIsNotNone(get_corpus_path("test"))  # corpus exists
        self.assertTrue(remove("test"))  # remove existing
        self.assertFalse(remove("test"))  # remove non-existing
        self.assertIsNone(get_corpus_path("XXXkdjfBzc"))  # query non-existing
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
            self.assertIsNotNone(download(name="test", version="0.0.11"))
        self.assertTrue(
            "Hash does not match expected."
            in
            str(context.exception)
        )
        self.assertIsNotNone(download(name="test", version="0.1"))
        self.assertIsNotNone(remove("test"))

    def test_tnc(self):
        self.assertIsNotNone(tnc.word_freqs())

    def test_ttc(self):
        self.assertIsNotNone(ttc.word_freqs())

    def test_wordnet(self):
        self.assertIsInstance(wordnet.langs(), list)
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
