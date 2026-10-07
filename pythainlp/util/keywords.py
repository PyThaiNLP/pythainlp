# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Keyword ranking functions for Thai text."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from pythainlp.corpus import thai_stopwords

_STOPWORDS: frozenset[str] = thai_stopwords()


def rank(
    words: list[str], exclude_stopwords: bool = False
) -> Optional[Counter[str]]:
    """
    Count word frequencies in a list of Thai words.

    Stopwords can be excluded from the count.

    :param list[str] words: list of words
    :param bool exclude_stopwords: exclude stopwords from the count if
        **True**, otherwise count them (default is **False**)
    :return: counter of word frequencies, or None if ``words`` is empty
    :rtype: Optional[collections.Counter[str]]

    :Example:

    Include stopwords when counting word frequencies:

        >>> from pythainlp.util import rank

        >>> words = [
        ...     "บันทึก",
        ...     "เหตุการณ์",
        ...     " ",
        ...     "มี",
        ...     "การ",
        ...     "บันทึก",
        ...     "เป็น",
        ...     " ",
        ...     "ลายลักษณ์อักษร",
        ... ]

        >>> rank(words)  # doctest: +NORMALIZE_WHITESPACE
        Counter({'บันทึก': 2, ' ': 2, 'เหตุการณ์': 1, 'มี': 1, 'การ': 1,
                 'เป็น': 1, 'ลายลักษณ์อักษร': 1})

    Exclude stopwords when counting word frequencies:

        >>> rank(words, exclude_stopwords=True)
        Counter({'บันทึก': 2, ' ': 2, 'เหตุการณ์': 1, 'ลายลักษณ์อักษร': 1})
    """
    if not words:
        return None

    if exclude_stopwords:
        words = [word for word in words if word not in _STOPWORDS]

    return Counter(words)


def find_keyword(word_list: list[str], min_len: int = 3) -> dict[str, int]:
    """
    Count word frequencies in a list of words, excluding stopwords.

    :param list[str] word_list: list of words
    :param int min_len: minimum frequency for a word to be retained
    :return: dictionary of words and their raw counts
    :rtype: dict[str, int]

    :Example:

        >>> from pythainlp.util import find_keyword

        >>> words = [
        ...     "บันทึก",
        ...     "เหตุการณ์",
        ...     "บันทึก",
        ...     "เหตุการณ์",
        ...     " ",
        ...     "มี",
        ...     "การ",
        ...     "บันทึก",
        ...     "เป็น",
        ...     " ",
        ...     "ลายลักษณ์อักษรและ",
        ...     "การ",
        ...     "บันทึก",
        ...     "เสียง",
        ...     "ใน",
        ...     "เหตุการณ์",
        ... ]

        >>> find_keyword(words)
        {'บันทึก': 4, 'เหตุการณ์': 3}

        >>> find_keyword(words, min_len=1)  # doctest: +NORMALIZE_WHITESPACE
        {'บันทึก': 4, 'เหตุการณ์': 3, ' ': 2, 'ลายลักษณ์อักษรและ': 1,
         'เสียง': 1}
    """
    word_counter = rank(word_list, exclude_stopwords=True)

    if word_counter is None:
        return {}

    return {k: v for k, v in word_counter.items() if v >= min_len}
