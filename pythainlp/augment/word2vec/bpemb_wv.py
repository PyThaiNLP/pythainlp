# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List, Tuple
from pythainlp.augment.word2vec.core import Word2VecAug


class BPEmbAug:
    """
    Thai Text Augment using word2vec from BPEmb

    BPEmb:
    `github.com/bheinzerling/bpemb <https://github.com/bheinzerling/bpemb>`_
    """

    def __init__(self, lang: str = "th", vs: int = 100000, dim: int = 300):
        from bpemb import BPEmb

        self.bpemb_temp = BPEmb(lang=lang, dim=dim, vs=vs)
        self.model = self.bpemb_temp.emb
        self.load_w2v()

    def tokenizer(self, text: str) -> List[str]:
        """
        :param str text: Thai text
        :rtype: List[str]
        """
        return self.bpemb_temp.encode(text)

    def load_w2v(self):
        """
        Load BPEmb model
        """
        self.aug = Word2VecAug(
            self.model, tokenize=self.tokenizer, type="model"
        )

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> List[Tuple[str]]:
        """
        Text Augment using word2vec from BPEmb

        :param str sentence: Thai sentence
        :param int n_sent: number of sentence
        :param float p: probability of word

        :return: list of synonyms
        :rtype: List[str]
        :Example:
        ::

            from pythainlp.augment.word2vec.bpemb_wv import BPEmbAug

            aug = BPEmbAug()
            aug.augment("ผมเรียน", n_sent=2, p=0.5)
            # output: ['ผมสอน', 'ผมเข้าเรียน']
        """
        self.sentence = sentence.replace(" ", "▁")
        self.temp = self.aug.augment(self.sentence, n_sent, p=p)
        self.temp_new = []
        for i in self.temp:
            self.t = ""
            for j in i:
                self.t += j.replace("▁", "")
            self.temp_new.append(self.t)
        return self.temp_new
