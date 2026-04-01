# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional

from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import thai2fit_tokenizer


class Thai2fitAug:
    """Text Augment using word2vec from Thai2Fit

    Thai2Fit:
    `github.com/cstorm125/thai2fit <https://github.com/cstorm125/thai2fit>`_
    """

    thai2fit_wv: Optional[str]
    aug: Word2VecAug

    def __init__(self) -> None:
        self.thai2fit_wv: Optional[str] = get_corpus_path("thai2fit_wv")
        self.load_w2v()

    def tokenizer(self, text: str) -> list[str]:
        """:param str text: Thai text
        :rtype: List[str]
        """
        tok = thai2fit_tokenizer()
        return tok.word_tokenize(text)

    def load_w2v(self) -> None:
        """Load Thai2Fit's word2vec model"""
        if not self.thai2fit_wv:
            raise FileNotFoundError(
                "corpus-not-found name='thai2fit_wv'\n"
                "  Corpus 'thai2fit_wv' not found.\n"
                "    Python: pythainlp.corpus.download('thai2fit_wv')\n"
                "    CLI:    thainlp data get thai2fit_wv"
            )
        self.aug: Word2VecAug = Word2VecAug(
            self.thai2fit_wv, self.tokenizer, type="binary"
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

            >>> from pythainlp.augment.word2vec import Thai2fitAug  # doctest: +SKIP

            >>> aug = Thai2fitAug()  # doctest: +SKIP
            >>> aug.augment("ผมเรียน", n_sent=2, p=0.5)  # doctest: +SKIP
            [('พวกเรา', 'เรียน'), ('ฉัน', 'เรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
