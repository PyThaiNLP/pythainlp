# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Text generator using n-gram language model

codes are from
https://towardsdatascience.com/understanding-word-n-grams-and-n-gram-probability-in-natural-language-processing-9d9eef0fa058
"""
import random
from typing import List, Union
from pythainlp.corpus.tnc import unigram_word_freqs as tnc_word_freqs_unigram
from pythainlp.corpus.tnc import bigram_word_freqs as tnc_word_freqs_bigram
from pythainlp.corpus.tnc import trigram_word_freqs as tnc_word_freqs_trigram
from pythainlp.corpus.ttc import unigram_word_freqs as ttc_word_freqs_unigram
from pythainlp.corpus.oscar import (
    unigram_word_freqs as oscar_word_freqs_unigram,
)


class Unigram:
    """
    Text generator using Unigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
        * *ttc* - Thai Textbook Corpus (TTC)
        * *oscar* - OSCAR Corpus
    """

    def __init__(self, name: str = "tnc"):
        if name == "tnc":
            self.counts = tnc_word_freqs_unigram()
        elif name == "ttc":
            self.counts = ttc_word_freqs_unigram()
        elif name == "oscar":
            self.counts = oscar_word_freqs_unigram()
        self.word = list(self.counts.keys())
        self.n = 0
        for i in self.word:
            self.n += self.counts[i]
        self.prob = {i: self.counts[i] / self.n for i in self.word}
        self._word_prob = {}

    def gen_sentence(
        self,
        start_seq: str = None,
        N: int = 3,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[List[str], str]:
        """
        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: List[str], str

        :Example:
        ::

            from pythainlp.generate import Unigram

            gen = Unigram()

            gen.gen_sentence("แมว")
            # output: 'แมวเวลานะนั้น'
        """
        if start_seq is None:
            start_seq = random.choice(self.word)
        rand_text = start_seq.lower()
        self._word_prob = {
            i: self.counts[i] / self.n
            for i in self.word
            if self.counts[i] / self.n >= prob
        }
        return self._next_word(
            rand_text, N, output_str, prob=prob, duplicate=duplicate
        )

    def _next_word(
        self,
        text: str,
        N: int,
        output_str: str,
        prob: float,
        duplicate: bool = False,
    ):
        self.words = []
        self.words.append(text)
        self._word_list = list(self._word_prob.keys())
        if N > len(self._word_list):
            N = len(self._word_list)
        for _ in range(N):
            self._word = random.choice(self._word_list)
            if duplicate is False:
                while self._word in self.words:
                    self._word = random.choice(self._word_list)
            self.words.append(self._word)

        if output_str:
            return "".join(self.words)
        return self.words


class Bigram:
    """
    Text generator using Bigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    def __init__(self, name: str = "tnc"):
        if name == "tnc":
            self.uni = tnc_word_freqs_unigram()
            self.bi = tnc_word_freqs_bigram()
        self.uni_keys = list(self.uni.keys())
        self.bi_keys = list(self.bi.keys())
        self.words = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str) -> float:
        """
        probability of word

        :param int t1: text 1
        :param int t2: text 2

        :return: probability value
        :rtype: float
        """
        try:
            v = self.bi[(t1, t2)] / self.uni[t1]
        except ZeroDivisionError:
            v = 0.0
        return v

    def gen_sentence(
        self,
        start_seq: str = None,
        N: int = 4,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[List[str], str]:
        """
        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: List[str], str

        :Example:
        ::

            from pythainlp.generate import Bigram

            gen = Bigram()

            gen.gen_sentence("แมว")
            # output: 'แมวไม่ได้รับเชื้อมัน'
        """
        if start_seq is None:
            start_seq = random.choice(self.words)
        self.late_word = start_seq
        self.list_word = []
        self.list_word.append(start_seq)

        for _ in range(N):
            if duplicate:
                self._temp = [
                    j for j in self.bi_keys if j[0] == self.late_word
                ]
            else:
                self._temp = [
                    j
                    for j in self.bi_keys
                    if j[0] == self.late_word and j[1] not in self.list_word
                ]
            self._probs = [
                self.prob(self.late_word, next_word[-1])
                for next_word in self._temp
            ]
            self._p2 = [j for j in self._probs if j >= prob]
            if len(self._p2) == 0:
                break
            self.items = self._temp[self._probs.index(random.choice(self._p2))]
            self.late_word = self.items[-1]
            self.list_word.append(self.late_word)
        if output_str:
            return "".join(self.list_word)
        return self.list_word


class Trigram:
    """
    Text generator using Trigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    def __init__(self, name: str = "tnc"):
        if name == "tnc":
            self.uni = tnc_word_freqs_unigram()
            self.bi = tnc_word_freqs_bigram()
            self.ti = tnc_word_freqs_trigram()
        self.uni_keys = list(self.uni.keys())
        self.bi_keys = list(self.bi.keys())
        self.ti_keys = list(self.ti.keys())
        self.words = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str, t3: str) -> float:
        """
        probability of word

        :param int t1: text 1
        :param int t2: text 2
        :param int t3: text 3

        :return: probability value
        :rtype: float
        """
        try:
            v = self.ti[(t1, t2, t3)] / self.bi[(t1, t2)]
        except ZeroDivisionError:
            v = 0.0

        return v

    def gen_sentence(
        self,
        start_seq: str = None,
        N: int = 4,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[List[str], str]:
        """
        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: List[str], str

        :Example:
        ::

            from pythainlp.generate import Trigram

            gen = Trigram()

            gen.gen_sentence()
            # output: 'ยังทำตัวเป็นเซิร์ฟเวอร์คือ'
        """
        if start_seq is None:
            start_seq = random.choice(self.bi_keys)
        self.late_word = start_seq
        self.list_word = []
        self.list_word.append(start_seq)

        for i in range(N):
            if duplicate:
                self._temp = [
                    j for j in self.ti_keys if j[:2] == self.late_word
                ]
            else:
                self._temp = [
                    j
                    for j in self.ti_keys
                    if j[:2] == self.late_word and j[1:] not in self.list_word
                ]
            self._probs = [
                self.prob(word[0], word[1], word[2]) for word in self._temp
            ]
            self._p2 = [j for j in self._probs if j >= prob]
            if len(self._p2) == 0:
                break
            self.items = self._temp[self._probs.index(random.choice(self._p2))]
            self.late_word = self.items[1:]
            self.list_word.append(self.late_word)
        self.listdata = []
        for i in self.list_word:
            for j in i:
                if j not in self.listdata:
                    self.listdata.append(j)
        if output_str:
            return "".join(self.listdata)
        return self.listdata
