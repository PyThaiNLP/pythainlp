# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text generator using n-gram language model

codes are from
https://towardsdatascience.com/understanding-word-n-grams-and-n-gram-probability-in-natural-language-processing-9d9eef0fa058
"""

from __future__ import annotations

import random
from typing import Union

from pythainlp.corpus.oscar import (
    unigram_word_freqs as oscar_word_freqs_unigram,
)
from pythainlp.corpus.tnc import bigram_word_freqs as tnc_word_freqs_bigram
from pythainlp.corpus.tnc import trigram_word_freqs as tnc_word_freqs_trigram
from pythainlp.corpus.tnc import unigram_word_freqs as tnc_word_freqs_unigram
from pythainlp.corpus.ttc import unigram_word_freqs as ttc_word_freqs_unigram


class Unigram:
    """Text generator using Unigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
        * *ttc* - Thai Textbook Corpus (TTC)
        * *oscar* - OSCAR Corpus
    """

    counts: dict[str, int]
    word: list[str]
    n: int
    prob: dict[str, float]
    _word_prob: dict[str, float]

    def __init__(self, name: str = "tnc") -> None:
        if name == "tnc":
            self.counts: dict[str, int] = tnc_word_freqs_unigram()
        elif name == "ttc":
            self.counts = ttc_word_freqs_unigram()
        elif name == "oscar":
            self.counts = oscar_word_freqs_unigram()
        self.word: list[str] = list(self.counts.keys())
        self.n: int = 0
        for i in self.word:
            self.n += self.counts[i]
        self.prob: dict[str, float] = {
            i: self.counts[i] / self.n for i in self.word
        }
        self._word_prob: dict[str, float] = {}

    def gen_sentence(
        self,
        start_seq: str = "",
        N: int = 3,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[list[str], str]:
        """Generate a sentence using the unigram model.

        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param float prob: minimum word probability threshold
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: Union[list[str], str]

        :Example:

            >>> from pythainlp.generate import Unigram  # doctest: +SKIP

            >>> gen = Unigram()  # doctest: +SKIP

            >>> gen.gen_sentence("แมว")  # doctest: +SKIP
            'แมวเวลานะนั้น'
        """
        if not start_seq:
            # Non-cryptographic use, pseudo-random generator is acceptable here
            start_seq = random.choice(self.word)  # noqa: S311
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
        output_str: bool,
        prob: float,
        duplicate: bool = False,
    ) -> Union[list[str], str]:
        words = []
        words.append(text)
        word_list = list(self._word_prob.keys())
        if N > len(word_list):
            N = len(word_list)
        for _ in range(N):
            # Non-cryptographic use, pseudo-random generator is acceptable here
            w = random.choice(word_list)  # noqa: S311
            if duplicate is False:
                while w in words:
                    w = random.choice(word_list)  # noqa: S311
            words.append(w)

        if output_str:
            return "".join(words)
        return words


class Bigram:
    """Text generator using Bigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    uni: dict[str, int]
    bi: dict[tuple[str, str], int]
    uni_keys: list[str]
    bi_keys: list[tuple[str, str]]
    words: list[str]

    def __init__(self, name: str = "tnc") -> None:
        if name == "tnc":
            self.uni: dict[str, int] = tnc_word_freqs_unigram()
            self.bi: dict[tuple[str, str], int] = tnc_word_freqs_bigram()
        self.uni_keys: list[str] = list(self.uni.keys())
        self.bi_keys: list[tuple[str, str]] = list(self.bi.keys())
        self.words: list[str] = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str) -> float:
        """Compute bigram probability P(t2 | t1).

        :param str t1: first word
        :param str t2: second word

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
        start_seq: str = "",
        N: int = 4,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[list[str], str]:
        """Generate a sentence using the bigram model.

        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param float prob: minimum word probability threshold
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: Union[list[str], str]

        :Example:

            >>> from pythainlp.generate import Bigram  # doctest: +SKIP

            >>> gen = Bigram()  # doctest: +SKIP

            >>> gen.gen_sentence("แมว")  # doctest: +SKIP
            'แมวไม่ได้รับเชื้อมัน'
        """
        if not start_seq:
            # Non-cryptographic use, pseudo-random generator is acceptable here
            start_seq = random.choice(self.words)  # noqa: S311
        late_word = start_seq
        list_word = []
        list_word.append(start_seq)

        for _ in range(N):
            if duplicate:
                temp = [j for j in self.bi_keys if j[0] == late_word]
            else:
                temp = [
                    j
                    for j in self.bi_keys
                    if j[0] == late_word and j[1] not in list_word
                ]
            probs = [self.prob(late_word, next_word[-1]) for next_word in temp]
            p2 = [j for j in probs if j >= prob]
            if len(p2) == 0:
                break
            # Non-cryptographic use, pseudo-random generator is acceptable here
            items = temp[probs.index(random.choice(p2))]  # noqa: S311
            late_word = items[-1]
            list_word.append(late_word)

        if output_str:
            return "".join(list_word)

        return list_word


class Trigram:
    """Text generator using Trigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    uni: dict[str, int]
    bi: dict[tuple[str, str], int]
    ti: dict[tuple[str, str, str], int]
    uni_keys: list[str]
    bi_keys: list[tuple[str, str]]
    ti_keys: list[tuple[str, str, str]]
    words: list[str]

    def __init__(self, name: str = "tnc") -> None:
        if name == "tnc":
            self.uni: dict[str, int] = tnc_word_freqs_unigram()
            self.bi: dict[tuple[str, str], int] = tnc_word_freqs_bigram()
            self.ti: dict[tuple[str, str, str], int] = tnc_word_freqs_trigram()
        self.uni_keys: list[str] = list(self.uni.keys())
        self.bi_keys: list[tuple[str, str]] = list(self.bi.keys())
        self.ti_keys: list[tuple[str, str, str]] = list(self.ti.keys())
        self.words: list[str] = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str, t3: str) -> float:
        """Compute trigram probability P(t3 | t1, t2).

        :param str t1: first word
        :param str t2: second word
        :param str t3: third word

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
        start_seq: Union[str, tuple[str, str]] = "",
        N: int = 4,
        prob: float = 0.001,
        output_str: bool = True,
        duplicate: bool = False,
    ) -> Union[list[str], str]:
        """Generate a sentence using the trigram model.

        :param start_seq: word or bigram to begin sentence with
        :type start_seq: Union[str, tuple[str, str]]
        :param int N: number of words
        :param float prob: minimum word probability threshold
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: Union[list[str], str]

        :Example:

            >>> from pythainlp.generate import Trigram  # doctest: +SKIP

            >>> gen = Trigram()  # doctest: +SKIP

            >>> gen.gen_sentence()  # doctest: +SKIP
            'ยังทำตัวเป็นเซิร์ฟเวอร์คือ'
        """
        late_word: Union[str, tuple[str, str]]
        if not start_seq:
            # Non-cryptographic use, pseudo-random generator is acceptable here
            start_seq = random.choice(self.bi_keys)  # noqa: S311
        late_word = start_seq
        list_word: list[Union[str, tuple[str, str]]] = []
        list_word.append(start_seq)

        for _ in range(N):
            if duplicate:
                temp = [j for j in self.ti_keys if j[:2] == late_word]
            else:
                temp = [
                    j
                    for j in self.ti_keys
                    if j[:2] == late_word and j[1:] not in list_word
                ]
            probs = [self.prob(word[0], word[1], word[2]) for word in temp]
            p2 = [j for j in probs if j >= prob]
            if len(p2) == 0:
                break
            # Non-cryptographic use, pseudo-random generator is acceptable here
            items = temp[probs.index(random.choice(p2))]  # noqa: S311
            late_word = items[1:]
            list_word.append(late_word)

        listdata: list[str] = []
        for item in list_word:
            if isinstance(item, tuple):
                for j in item:
                    if j not in listdata:
                        listdata.append(j)
            elif isinstance(item, str) and item not in listdata:
                listdata.append(item)

        if output_str:
            return "".join(listdata)

        return listdata
