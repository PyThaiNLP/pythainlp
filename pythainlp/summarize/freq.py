# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Summarization by frequency of words"""

from __future__ import annotations

from collections import defaultdict
from heapq import nlargest
from string import punctuation
from typing import cast

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import sent_tokenize, word_tokenize

_STOPWORDS: frozenset[str] = thai_stopwords()


class FrequencySummarizer:
    __min_cut: float
    __max_cut: float
    __stopwords: set[str]
    __freq: "defaultdict[str, float]"

    def __init__(self, min_cut: float = 0.1, max_cut: float = 0.9) -> None:
        self.__min_cut: float = min_cut
        self.__max_cut: float = max_cut
        self.__stopwords: set[str] = set(punctuation).union(_STOPWORDS)

    @staticmethod
    def __rank(ranking: dict[int, float], n: int) -> list[int]:
        return nlargest(n, ranking, key=lambda idx: ranking[idx])

    def __compute_frequencies(
        self, word_tokenized_sents: list[list[str]]
    ) -> defaultdict[str, int]:
        word_freqs: defaultdict[str, int] = defaultdict(int)
        for sent in word_tokenized_sents:
            for word in sent:
                if word not in self.__stopwords:
                    word_freqs[word] += 1

        max_freq = max(word_freqs.values())
        for w in list(word_freqs):
            word_freqs[w] = word_freqs[w] // max_freq
            if (
                word_freqs[w] >= self.__max_cut
                or word_freqs[w] <= self.__min_cut
            ):
                del word_freqs[w]

        return word_freqs

    def summarize(
        self, text: str, n: int, tokenizer: str = "newmm"
    ) -> list[str]:
        # sent_tokenize with str input returns list[str]
        sents = cast(
            "list[str]", sent_tokenize(text, engine="whitespace+newline")
        )
        word_tokenized_sents = [
            word_tokenize(sent, engine=tokenizer) for sent in sents
        ]
        self.__freq: "defaultdict[str, float]" = self.__(
            word_tokenized_sents
        )
        ranking: defaultdict[int, float] = defaultdict(int)

        for i, sent in enumerate(word_tokenized_sents):
            for w in sent:
                if w in self.__freq:
                    ranking[i] += self.__freq[w]
        summaries_idx = self.__rank(ranking, n)

        return [sents[j] for j in summaries_idx]
