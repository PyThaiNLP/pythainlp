# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Summarize text by word frequency."""

from __future__ import annotations

from collections import Counter
from heapq import nlargest
from string import punctuation
from typing import cast

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import sent_tokenize, word_tokenize

_STOPWORDS: frozenset[str] = thai_stopwords()


class FrequencySummarizer:
    """Summarize text by word frequency."""

    __min_cut: float
    __max_cut: float
    __stopwords: set[str]
    __freq: dict[str, float]

    def __init__(self, min_cut: float = 0.1, max_cut: float = 0.9) -> None:
        """
        Initialize the frequency summarizer.

        :param float min_cut: minimum normalized word frequency to count
        :param float max_cut: maximum normalized word frequency to count
        """
        self.__min_cut: float = min_cut
        self.__max_cut: float = max_cut
        self.__stopwords: set[str] = set(punctuation).union(_STOPWORDS)

    def __compute_frequencies(
        self, word_tokenized_sents: list[list[str]]
    ) -> dict[str, float]:
        counts: Counter[str] = Counter()
        for sent in word_tokenized_sents:
            for word in sent:
                if word not in self.__stopwords:
                    counts[word] += 1

        if not counts:
            return {}

        max_freq = float(max(counts.values()))
        freqs = {w: (c / max_freq) for w, c in counts.items()}
        return {
            w: f
            for w, f in freqs.items()
            if self.__min_cut < f < self.__max_cut
        }

    def summarize(
        self, text: str, n: int, tokenizer: str = "newmm"
    ) -> list[str]:
        """
        Summarize text by selecting the highest scoring sentences.

        :param str text: text to summarize
        :param int n: number of sentences in the summary
        :param str tokenizer: engine to tokenize text with
        :return: list of selected sentences
        :rtype: list[str]
        """
        # sent_tokenize with str input returns list[str]
        sents = cast(
            "list[str]", sent_tokenize(text, engine="whitespace+newline")
        )
        word_tokenized_sents = [
            word_tokenize(sent, engine=tokenizer) for sent in sents
        ]
        self.__freq = self.__compute_frequencies(word_tokenized_sents)
        scores = [0.0] * len(word_tokenized_sents)
        for i, sent in enumerate(word_tokenized_sents):
            scores[i] = sum(self.__freq.get(w, 0.0) for w in sent)
        summaries_idx = nlargest(n, range(len(scores)), key=scores.__getitem__)
        return [sents[j] for j in summaries_idx]
