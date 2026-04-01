# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from collections import Counter
from typing import Optional

from pythainlp.corpus import thai_stopwords

_STOPWORDS: frozenset[str] = thai_stopwords()


def rank(
    words: list[str], exclude_stopwords: bool = False
) -> Optional[Counter[str]]:
    """Count word frequencies given a list of Thai words with an option
    to exclude stopwords.

    :param list words: a list of words
    :param bool exclude_stopwords: If this parameter is set to **True**,
                                   exclude stopwords from counting.
                                   Otherwise, the stopwords will be counted.
                                   By default, `exclude_stopwords`is
                                   set to **False**
    :return: a Counter object representing word frequencies in the text,
             or None if `words` is empty
    :rtype: Optional[collections.Counter[str]]

    :Example:

    Include stopwords when counting word frequencies:

        >>> from pythainlp.util import rank  # doctest: +SKIP

        >>> words = ["บันทึก", "เหตุการณ์", " ", "มี", "การ", "บันทึก",  # doctest: +SKIP
        ... "เป็น", " ", "ลายลักษณ์อักษร"]

        >>> rank(words)  # doctest: +SKIP
        Counter(
            {
                ' ': 2,
                'การ': 1,
                'บันทึก': 2,
                'มี': 1,
                'ลายลักษณ์อักษร': 1,
                'เป็น': 1,
                'เหตุการณ์': 1
            })

    Exclude stopwords when counting word frequencies:

        >>> from pythainlp.util import rank  # doctest: +SKIP

        >>> words = ["บันทึก", "เหตุการณ์", " ", "มี", "การ", "บันทึก",  # doctest: +SKIP
        ...     "เป็น", " ", "ลายลักษณ์อักษร"]

        >>> rank(words)  # doctest: +SKIP
        Counter(
            {
                ' ': 2,
                'บันทึก': 2,
                'ลายลักษณ์อักษร': 1,
                'เหตุการณ์': 1
            })
    """
    if not words:
        return None

    if exclude_stopwords:
        words = [word for word in words if word not in _STOPWORDS]

    return Counter(words)


def find_keyword(word_list: list[str], min_len: int = 3) -> dict[str, int]:
    """Counts the frequencies of words in the list
    where stopwords are excluded and returns a frequency dictionary.

    :param list word_list: a list of words
    :param int min_len: the minimum frequency for words to be retained

    :return: a dictionary object with key-value pair being words and their raw counts
    :rtype: dict[str, int]

    :Example:

        >>> from pythainlp.util import find_keyword  # doctest: +SKIP

        >>> words = ["บันทึก", "เหตุการณ์", "บันทึก", "เหตุการณ์",  # doctest: +SKIP
        ...          " ", "มี", "การ", "บันทึก", "เป็น", " ", "ลายลักษณ์อักษร"
        ...          "และ", "การ", "บันทึก","เสียง","ใน","เหตุการณ์"]

        >>> find_keyword(words)  # doctest: +SKIP
        {'บันทึก': 4, 'เหตุการณ์': 3}

        >>> find_keyword(words, min_len=1)  # doctest: +SKIP
        {' ': 2, 'บันทึก': 4, 'ลายลักษณ์อักษรและ': 1,
                 'เสียง': 1, 'เหตุการณ์': 3}
    """
    word_counter = rank(word_list, exclude_stopwords=True)

    if word_counter is None:
        return {}

    return {k: v for k, v in word_counter.items() if v >= min_len}
