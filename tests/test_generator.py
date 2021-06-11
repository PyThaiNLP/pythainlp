# -*- coding: utf-8 -*-

import unittest

from pythainlp.generator import Unigram, Bigram, Tigram
from pythainlp.generator.thai2fit import gen_sentence


class TestGeneratorPackage(unittest.TestCase):
    def test_unigram(self):
        _tnc_unigram = Unigram("tnc")
        self.assertIsNotNone(_tnc_unigram.gen_sentence("ผมชอบไปโรงเรียน"))
        _ttc_unigram = Unigram("ttc")
        self.assertIsNotNone(_ttc_unigram.gen_sentence("ผมชอบไปโรงเรียน"))
        _oscar_unigram = Unigram("oscar")
        self.assertIsNotNone(_oscar_unigram.gen_sentence("ผมชอบไปโรงเรียน"))

    def test_bigram(self):
        _bigram = Bigram()
        self.assertIsNotNone(_bigram.gen_sentence("ผมชอบไปโรงเรียน"))

    def test_tigram(self):
        _tigram = Tigram()
        self.assertIsNotNone(_tigram.gen_sentence("ผมชอบไปโรงเรียน"))

    def test_thai2fit(self):
        self.assertIsNotNone(gen_sentence("ผมชอบไปโรงเรียน"))
