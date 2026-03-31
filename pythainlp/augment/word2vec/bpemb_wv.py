# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pythainlp.augment.word2vec.core import Word2VecAug

if TYPE_CHECKING:
    from bpemb import BPEmb
    from gensim.models.keyedvectors import KeyedVectors


class BPEmbAug:
    """Thai Text Augment using word2vec from BPEmb

    BPEmb:
    `github.com/bheinzerling/bpemb <https://github.com/bheinzerling/bpemb>`_
    """

    bpemb_temp: BPEmb
    model: KeyedVectors
    aug: Word2VecAug
    sentence: str
    temp: list[tuple[str, ...]]
    temp_new: list[str]
    t: str

    def __init__(
        self, lang: str = "th", vs: int = 100000, dim: int = 300
    ) -> None:
        from bpemb import BPEmb

        self.bpemb_temp: BPEmb = BPEmb(lang=lang, dim=dim, vs=vs)
        self.model: KeyedVectors = self.bpemb_temp.emb
        self.load_w2v()

    def tokenizer(self, text: str) -> list[str]:
        """:param str text: Thai text
        :rtype: List[str]
        """
        return cast(list[str], self.bpemb_temp.encode(text))

    def load_w2v(self) -> None:
        """Load BPEmb model"""
        self.aug: Word2VecAug = Word2VecAug(
            self.model, tokenize=self.tokenizer, type="model"
        )

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> list[str]:
        """Text Augment using word2vec from BPEmb

        :param str sentence: Thai sentence
        :param int n_sent: number of sentence
        :param float p: probability of word

        :return: list of synonyms
        :rtype: list[str]
        :Example:

            >>> from pythainlp.augment.word2vec.bpemb_wv import BPEmbAug  # doctest: +SKIP

            >>> aug = BPEmbAug()  # doctest: +SKIP
            >>> aug.augment("ผมเรียน", n_sent=2, p=0.5)  # doctest: +SKIP
            ['ผมสอน', 'ผมเข้าเรียน']
        """
        self.sentence: str = sentence.replace(" ", "▁")
        self.temp: list[tuple[str, ...]] = self.aug.augment(
            self.sentence, n_sent, p=p
        )
        self.temp_new: list[str] = []
        for i in self.temp:
            self.t: str = ""
            for j in i:
                self.t += j.replace("▁", "")
            self.temp_new.append(self.t)
        return self.temp_new
