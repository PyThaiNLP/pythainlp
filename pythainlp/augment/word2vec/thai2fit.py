# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import THAI2FIT_TOKENIZER
from typing import List, Tuple


class Thai2fitAug:
    """
    Text Augment using word2vec from Thai2Fit

    Thai2Fit:
    `github.com/cstorm125/thai2fit <https://github.com/cstorm125/thai2fit>`_
    """

    def __init__(self):
        self.thai2fit_wv = get_corpus_path("thai2fit_wv")
        self.load_w2v()

    def tokenizer(self, text: str) -> List[str]:
        """
        :param str text: thai text
        :rtype: List[str]
        """
        return THAI2FIT_TOKENIZER.word_tokenize(text)

    def load_w2v(self):
        """
        Load thai2fit word2vec model
        """
        self.aug = Word2VecAug(self.thai2fit_wv, self.tokenizer, type="binary")

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> List[Tuple[str]]:
        """
        Text Augment using word2vec from Thai2Fit

        :param str sentence: thai sentence
        :param int n_sent: number sentence
        :param float p: Probability of word

        :return: list of text augment
        :rtype: List[Tuple[str]]

        :Example:
        ::

            from pythainlp.augment.word2vec import Thai2fitAug

            aug = Thai2fitAug()
            aug.augment("ผมเรียน", n_sent=2, p=0.5)
            # output: [('พวกเรา', 'เรียน'), ('ฉัน', 'เรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
