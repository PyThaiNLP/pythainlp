# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from collections import defaultdict
from heapq import nlargest
from string import punctuation

from pythainlp.corpus import stopwords
from pythainlp.tokenize import sent_tokenize, word_tokenize


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self.__min_cut = min_cut
        self.__max_cut = max_cut
        self.__stopwords = set(stopwords.words("thai") + list(punctuation))

    def __compute_frequencies(self, word_tokenized_sents):
        word_freqs = defaultdict(int)
        for sent in word_tokenized_sents:
            for word in sent:
                if word not in self.__stopwords:
                    word_freqs[word] += 1

        max_freq = float(max(word_freqs.values()))
        for w in list(word_freqs):
            word_freqs[w] = word_freqs[w] / max_freq
            if word_freqs[w] >= self.__max_cut or word_freqs[w] <= self.__min_cut:
                del word_freqs[w]

        return word_freqs

    def __rank(self, ranking, n):
        return nlargest(n, ranking, key=ranking.get)

    def summarize(self, text, n, tokenizer):
        sents = sent_tokenize(text)
        word_tokenized_sents = [word_tokenize(sent, tokenizer) for sent in sents]
        self.__freq = self.__compute_frequencies(word_tokenized_sents)
        ranking = defaultdict(int)

        for i, sent in enumerate(word_tokenized_sents):
            for w in sent:
                if w in self.__freq:
                    ranking[i] += self.__freq[w]
        summaries_idx = self.__rank(ranking, n)

        return [sents[j] for j in summaries_idx]


def summarize_text(text, n, engine="frequency", tokenizer="newmm"):
    """
    Thai text summarization
    :param str text: text to be summarized
    :param int n: number of sentences to be included in the summary
    :param str engine: text summarization engine
    :param str tokenizer: word tokenizer
    :return List[str] summary: list of selected sentences
    """
    sents = []

    if engine == "frequency":
        sents = FrequencySummarizer().summarize(text, n, tokenizer)
    else:  # if engine not found, return first n sentences
        sents = sent_tokenize(text)[:n]

    return sents
