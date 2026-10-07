# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Augment Thai text using word2vec from LTW2V."""

from __future__ import annotations

from typing import Optional

from pythainlp.augment.word2vec.core import Word2VecAug
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import word_tokenize


class LTW2VAug:
    """
    Augment Thai text using word2vec from LTW2V.

    LTW2V:
    `github.com/PyThaiNLP/large-thaiword2vec
    <https://github.com/PyThaiNLP/large-thaiword2vec>`_
    """

    ltw2v_wv: Optional[str]
    aug: Word2VecAug

    def __init__(self) -> None:
        """Initialize the LTW2V word2vec augmenter."""
        self.ltw2v_wv: Optional[str] = get_corpus_path("ltw2v")
        self.load_w2v()

    def tokenizer(self, text: str) -> list[str]:
        """
        Tokenize text into a list of words.

        :param str text: Thai text to tokenize
        :return: list of words
        :rtype: list[str]
        """
        return word_tokenize(text, engine="newmm")

    def load_w2v(self) -> None:  # insert substitute
        """Load the LTW2V word2vec model."""
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
        """
        Augment text using word2vec from LTW2V.

        :param str sentence: Thai text to augment
        :param int n_sent: number of augmented sentences
        :param float p: minimum similarity score of a replacement word

        :return: list of augmented sentences, each a tuple of words
        :rtype: list[tuple[str, ...]]

        :Example:

            >>> from pythainlp.augment.word2vec import (
            ...     LTW2VAug,
            ... )  # doctest: +SKIP

            >>> aug = LTW2VAug()  # doctest: +SKIP
            >>> aug.augment("ผมเรียน", n_sent=2, p=0.5)  # doctest: +SKIP
            [('เขา', 'เรียนหนังสือ'), ('เขา', 'สมัครเรียน')]
        """
        return self.aug.augment(sentence, n_sent, p)
