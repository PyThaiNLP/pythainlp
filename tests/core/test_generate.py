# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.generate import Bigram, Trigram, Unigram


class GenerateTestCase(unittest.TestCase):
    def test_unigram(self):
        tnc_unigram = Unigram("tnc")
        self.assertIsNotNone(tnc_unigram.gen_sentence())
        self.assertIsNotNone(tnc_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(tnc_unigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(tnc_unigram.gen_sentence(duplicate=True))

        ttc_unigram = Unigram("ttc")
        self.assertIsNotNone(ttc_unigram.gen_sentence())
        self.assertIsNotNone(ttc_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(ttc_unigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(ttc_unigram.gen_sentence(duplicate=True))

        oscar_unigram = Unigram("oscar")
        self.assertIsNotNone(oscar_unigram.gen_sentence())
        self.assertIsNotNone(oscar_unigram.gen_sentence("ผม"))
        self.assertIsNotNone(
            oscar_unigram.gen_sentence("ผม", output_str=False)
        )
        self.assertIsNotNone(oscar_unigram.gen_sentence(duplicate=True))

    def test_bigram(self):
        bigram = Bigram()
        self.assertIsNotNone(bigram.gen_sentence())
        self.assertIsNotNone(bigram.gen_sentence("ผม"))
        self.assertIsNotNone(bigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(bigram.gen_sentence(duplicate=True))

    def test_trigram(self):
        trigram = Trigram()
        self.assertIsNotNone(trigram.gen_sentence())
        self.assertIsNotNone(trigram.gen_sentence("ผม"))
        self.assertIsNotNone(trigram.gen_sentence("ผม", output_str=False))
        self.assertIsNotNone(trigram.gen_sentence(duplicate=True))
