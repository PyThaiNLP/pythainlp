# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional

from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import word_tokenize


class LTW2VAug:
    """Text Augment using word2vec from LTW2V

    LTW2V:
    `github.com/PyThaiNLP/large-thaiword2vec <https://github.com/PyThaiNLP/large-thaiword2vec>`_
    """

    ltw2v_wv: Optional[str]
    aug: Word2VecAug

    def __init__(self) -> None:
        self.ltw2v_wv: Optional[str] = get_corpus_path("ltw2v")
        self.load_w2v()

    def tokenizer(self, text: str) -> list[str]:
        """:param str text: Thai text
        :rtype: List[str]
        """
        return word_tokenize(text, engine="newmm")

    def load_w2v(self) -> None:  # insert substitute
        """Load LTW2V's word2vec model"""
        if not self.ltw2v_wv:
            raise FileNotFoundError(
                "corpus-not-found name='ltw2v_wv'\n"
                "  Corpus 'ltw2v_wv' not found.\n"
                "    Python: pythainlp.corpus.download('ltw2v_wv')\n"
                "    CLI:    thainlp data get ltw2v_wv"
            )
        self.aug: Word2VecAug = Word2VecAug(
            self.ltw2v_wv, self.tokenizer, type="binary"
        )

    def augment(
        self, sentence: str, n_sent: int = 1, p: float = 0.7
    ) -> list[tuple[str, ...]]:
        """Text Augment using word2vec from Thai2Fit

        :param str sentence: Thai sentence
        :param int n_sent: number of sentence
        :param float p: probability of word

        :return: list of text augmented
        :rtype: List[Tuple[str]]

        :Example:

            >>> from pythainlp.augment.word2vec import LTW2VAug  # doctest: +SKIP

            >>> aug = LTW2VAug()  # doctest: +SKIP
            >>> aug.augment("ผมเรียน", n_sent=2, p=0.5)  # doctest: +SKIP
            [('เขา', 'เรียนหนังสือ'), ('เขา', 'สมัครเรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
