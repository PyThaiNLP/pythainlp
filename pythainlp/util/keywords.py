# -*- coding: utf-8 -*-
from collections import Counter
from typing import Dict, List

from pythainlp.corpus import thai_stopwords

_STOPWORDS = thai_stopwords()


def rank(words: List[str], exclude_stopwords: bool = False) -> Counter:
    """
    Sort words by frequency

    :param list words: a list of words
    :param bool exclude_stopwords: exclude stopwords
    :return: Counter
    """
    if not words:
        return None

    if exclude_stopwords:
        words = [word for word in words if word not in _STOPWORDS]

    return Counter(words)


def find_keyword(word_list: List[str], min_len: int = 3) -> Dict[str, int]:
    """
    :param list word_list: a list of words
    :param int min_len: a mininum length of keywords to look for
    :return: dict
    """
    word_list = rank(word_list, exclude_stopwords=True)

    return {k: v for k, v in word_list.items() if v >= min_len}
