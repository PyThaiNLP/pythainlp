# -*- coding: utf-8 -*-
from pythainlp.corpus import thai_stopwords
from pythainlp.util import rank

_STOPWORDS = thai_stopwords()


def find_keyword(word_list, lentext=3):
    """
    :param list word_list: a list of Thai words
    :param int lentext: a number of keywords to look for
    :return: dict
    """
    filtered_words = [word for word in word_list if word not in _STOPWORDS]
    word_list = rank(filtered_words)
    return {k: v for k, v in word_list.items() if v >= lentext}
