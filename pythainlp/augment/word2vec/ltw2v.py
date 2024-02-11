# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List, Tuple
from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import word_tokenize


class LTW2VAug:
    """
    Text Augment using word2vec from LTW2V

    LTW2V:
    `github.com/PyThaiNLP/large-thaiword2vec <https://github.com/PyThaiNLP/large-thaiword2vec>`_
    """

    def __init__(self):
        self.ltw2v_wv = get_corpus_path("ltw2v")
        self.load_w2v()

    def tokenizer(self, text: str) -> List[str]:
        """
        :param str text: Thai text
        :rtype: List[str]
        """
        return word_tokenize(text, engine="newmm")

    def load_w2v(self):  # insert substitute
        """
        Load LTW2V's word2vec model
        """
        self.aug = Word2VecAug(self.ltw2v_wv, self.tokenizer, type="binary")

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> List[Tuple[str]]:
        """
        Text Augment using word2vec from Thai2Fit

        :param str sentence: Thai sentence
        :param int n_sent: number of sentence
        :param float p: probability of word

        :return: list of text augmented
        :rtype: List[Tuple[str]]

        :Example:
        ::

            from pythainlp.augment.word2vec import LTW2VAug

            aug = LTW2VAug()
            aug.augment("ผมเรียน", n_sent=2, p=0.5)
            # output: [('เขา', 'เรียนหนังสือ'), ('เขา', 'สมัครเรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
