# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from collections import Counter
from typing import Dict, List

from pythainlp.corpus import thai_stopwords

_STOPWORDS = thai_stopwords()


def rank(words: List[str], exclude_stopwords: bool = False) -> Counter:
    """
    Count word frequencies given a list of Thai words with an option
    to exclude stopwords.

    :param list words: a list of words
    :param bool exclude_stopwords: If this parameter is set to **True**,
                                   exclude stopwords from counting.
                                   Otherwise, the stopwords will be counted.
                                   By default, `exclude_stopwords`is
                                   set to **False**
    :return: a Counter object representing word frequencies in the text
    :rtype: :class:`collections.Counter`

    :Example:

    Include stopwords when counting word frequencies::

        from pythainlp.util import rank

        words = ["บันทึก", "เหตุการณ์", " ", "มี", "การ", "บันทึก", \\
        "เป็น", " ", "ลายลักษณ์อักษร"]

        rank(words)
        # output:
        # Counter(
        #     {
        #         ' ': 2,
        #         'การ': 1,
        #         'บันทึก': 2,
        #         'มี': 1,
        #         'ลายลักษณ์อักษร': 1,
        #         'เป็น': 1,
        #         'เหตุการณ์': 1
        #     })

    Exclude stopwords when counting word frequencies::

        from pythainlp.util import rank

        words = ["บันทึก", "เหตุการณ์", " ", "มี", "การ", "บันทึก", \\
            "เป็น", " ", "ลายลักษณ์อักษร"]

        rank(words)
        # output:
        # Counter(
        #     {
        #         ' ': 2,
        #         'บันทึก': 2,
        #         'ลายลักษณ์อักษร': 1,
        #         'เหตุการณ์': 1
        #     })
    """
    if not words:
        return None

    if exclude_stopwords:
        words = [word for word in words if word not in _STOPWORDS]

    return Counter(words)


def find_keyword(word_list: List[str], min_len: int = 3) -> Dict[str, int]:
    """
    This function counts the frequencies of words in the list
    where stopword is excluded and returns a frequency dictionary.

    :param list word_list: a list of words
    :param int min_len: the minimum frequency for words to be retained

    :return: a dictionary object with key-value pair being words and their raw counts
    :rtype: dict[str, int]

    :Example:
    ::

        from pythainlp.util import find_keyword

        words = ["บันทึก", "เหตุการณ์", "บันทึก", "เหตุการณ์",
                 " ", "มี", "การ", "บันทึก", "เป็น", " ", "ลายลักษณ์อักษร"
                 "และ", "การ", "บันทึก","เสียง","ใน","เหตุการณ์"]

        find_keyword(words)
        # output: {'บันทึก': 4, 'เหตุการณ์': 3}

        find_keyword(words, min_len=1)
        # output: {' ': 2, 'บันทึก': 4, 'ลายลักษณ์อักษรและ': 1,
         'เสียง': 1, 'เหตุการณ์': 3}
    """
    word_list = rank(word_list, exclude_stopwords=True)

    return {k: v for k, v in word_list.items() if v >= min_len}
