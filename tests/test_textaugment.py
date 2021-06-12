# -*- coding: utf-8 -*-

import unittest
from pythainlp.textaugment import WordNetAug
from pythainlp.textaugment.lm import Thai2transformersAug
from pythainlp.textaugment.word2vec import (
    Thai2fitAug,
    BPEmbAug
)

class TestTextaugmentPackage(unittest.TestCase):
    def setup(self):
        self.text = "เรารักคุณมากที่สุดในโลก"
        self.text2 = "เราอยู่ที่มหาวิทยาลัยขอนแก่น"

    def test_WordNetAug(self):
        wordnetaug = WordNetAug()
        self.assertIsNotNone(wordnetaug.augment(self.text))

    def test_Thai2fitAug(self):
        _aug = Thai2fitAug()
        self.assertIsNotNone(_aug.tokenizer(self.text))
        self.assertIsNotNone(_aug.augment(self.text, n_sent=3, p = 0.5))

    def test_Thai2transformersAug(self):
        _aug = Thai2transformersAug()
        self.assertIsNotNone(_aug.augment(self.text2, num_replace_tokens=1))
