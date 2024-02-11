# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
import nltk
from pythainlp.augment import WordNetAug
from pythainlp.augment.wordnet import postype2wordnet
# from pythainlp.augment.lm import Thai2transformersAug
# from pythainlp.augment.lm.phayathaibert import ThaiTextAugmenter
from pythainlp.augment.word2vec.bpemb_wv import BPEmbAug
from pythainlp.augment.word2vec import (
    LTW2VAug
)


class TestTextaugmentPackage(unittest.TestCase):
    def setUp(self):
        self.text = "เรารักคุณมากที่สุดในโลก"
        self.text2 = "เราอยู่ที่มหาวิทยาลัยขอนแก่น"

    def test_WordNetAug(self):
        nltk.download('omw-1.4', force=True)  # load wordnet
        wordnetaug = WordNetAug()
        self.assertIsNotNone(wordnetaug.augment(self.text))
        self.assertIsNotNone(wordnetaug.find_synonyms("ผม", pos=None))
        self.assertIsNotNone(wordnetaug.augment(self.text, postag=False))
        self.assertIsNone(postype2wordnet('n', 'abc'))
        self.assertIsNotNone(postype2wordnet('NOUN', 'orchid'))

    # def test_Thai2fitAug(self):
    #     _aug = Thai2fitAug()
    #     self.assertIsNotNone(_aug.tokenizer(self.text))
    #     self.assertIsNotNone(_aug.augment(self.text, n_sent=3, p=0.5))

    def test_BPEmbAug(self):
        _aug = BPEmbAug()
        self.assertIsNotNone(_aug.tokenizer(self.text))
        self.assertIsNotNone(_aug.augment(self.text, n_sent=3, p=0.5))

    def test_LTW2VAug(self):
        _aug = LTW2VAug()
        self.assertIsNotNone(_aug.tokenizer(self.text))
        self.assertIsNotNone(_aug.augment(self.text, n_sent=3, p=0.5))

    # def test_Thai2transformersAug(self):
    #     _aug = Thai2transformersAug()
    #     self.assertIsNotNone(_aug.augment(self.text2, num_replace_tokens=1))

    # def test_ThaiTextAugmenter(self):
    #     _aug = ThaiTextAugmenter()
    #     self.assertIsNotNone(_aug.augment(self.text2, num__augs=3))
