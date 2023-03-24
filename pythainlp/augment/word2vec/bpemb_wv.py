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
from typing import List, Tuple


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
        :param str text: thai text
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

        :param str sentence: thai sentence
        :param int n_sent: number sentence
        :param float p: Probability of word

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
