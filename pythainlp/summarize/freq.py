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
"""
Summarization by frequency of words
"""
from collections import defaultdict
from heapq import nlargest
from string import punctuation
from typing import List

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import sent_tokenize, word_tokenize

_STOPWORDS = thai_stopwords()


class FrequencySummarizer:
    def __init__(self, min_cut: float = 0.1, max_cut: float = 0.9):
        self.__min_cut = min_cut
        self.__max_cut = max_cut
        self.__stopwords = set(punctuation).union(_STOPWORDS)

    @staticmethod
    def __rank(ranking, n: int):
        return nlargest(n, ranking, key=ranking.get)

    def __compute_frequencies(
        self, word_tokenized_sents: List[List[str]]
    ) -> defaultdict:
        word_freqs = defaultdict(int)
        for sent in word_tokenized_sents:
            for word in sent:
                if word not in self.__stopwords:
                    word_freqs[word] += 1

        max_freq = float(max(word_freqs.values()))
        for w in list(word_freqs):
            word_freqs[w] = word_freqs[w] / max_freq
            if (
                word_freqs[w] >= self.__max_cut
                or word_freqs[w] <= self.__min_cut
            ):
                del word_freqs[w]

        return word_freqs

    def summarize(
        self, text: str, n: int, tokenizer: str = "newmm"
    ) -> List[str]:
        sents = sent_tokenize(text, engine="whitespace+newline")
        word_tokenized_sents = [
            word_tokenize(sent, engine=tokenizer) for sent in sents
        ]
        self.__freq = self.__compute_frequencies(word_tokenized_sents)
        ranking = defaultdict(int)

        for i, sent in enumerate(word_tokenized_sents):
            for w in sent:
                if w in self.__freq:
                    ranking[i] += self.__freq[w]
        summaries_idx = self.__rank(ranking, n)

        return [sents[j] for j in summaries_idx]
