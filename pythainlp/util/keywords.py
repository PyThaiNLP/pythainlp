# -*- coding: utf-8 -*-
from typing import Dict, List

from pythainlp.util import rank


def find_keyword(word_list: List[str], min_len: int = 3) -> Dict[str, int]:
    """
    :param list word_list: a list of words
    :param int min_len: a mininum length of keywords to look for
    :return: dict
    """
    word_list = rank(word_list, exclude_stopword=True)

    return {k: v for k, v in word_list.items() if v >= min_len}
