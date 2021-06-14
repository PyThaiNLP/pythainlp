# -*- coding: utf-8 -*-

import unittest

from pythainlp.generate import Unigram, Bigram, Tigram
from pythainlp.generate.thai2fit import gen_sentence


class TestGeneratePackage(unittest.TestCase):
    def test_unigram(self):
        _tnc_unigram = Unigram("tnc")
        self.assertIsNotNone(_tnc_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(_tnc_unigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(_tnc_unigram.gen_sentence())
        self.assertIsNotNone(_tnc_unigram.gen_sentence(duplicate=True))
        _ttc_unigram = Unigram("ttc")
        self.assertIsNotNone(_ttc_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(_ttc_unigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(_ttc_unigram.gen_sentence())
        self.assertIsNotNone(_ttc_unigram.gen_sentence(duplicate=True))
        _oscar_unigram = Unigram("oscar")
        self.assertIsNotNone(_oscar_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(
            _oscar_unigram.gen_sentence("ผม", output_str=False)
        )
        self.assertIsNotNone(_oscar_unigram.gen_sentence())
        self.assertIsNotNone(_oscar_unigram.gen_sentence(duplicate=True))

    def test_bigram(self):
        _bigram = Bigram()
        self.assertIsNotNone(_bigram.gen_sentence("ผม"))
        self.assertIsNotNone(_bigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(_bigram.gen_sentence())
        self.assertIsNotNone(_bigram.gen_sentence(duplicate=True))

    def test_tigram(self):
        _tigram = Tigram()
        self.assertIsNotNone(_tigram.gen_sentence("ผม"))
        self.assertIsNotNone(_tigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(_tigram.gen_sentence())
        self.assertIsNotNone(_tigram.gen_sentence(duplicate=True))

    def test_thai2fit(self):
        self.assertIsNotNone(gen_sentence("กาลครั้งหนึ่งนานมาแล้ว"))
        self.assertIsNotNone(gen_sentence())
