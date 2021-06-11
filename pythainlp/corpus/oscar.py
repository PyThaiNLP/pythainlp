# -*- coding: utf-8 -*-
"""
Thai unigram word frequency from OSCAR Corpus (icu word tokenize)

Credit: Korakot Chaovavanich
https://web.facebook.com/groups/colab.thailand/permalink/1524070061101680/
"""

__all__ = [
    "word_freqs",
    "unigram_word_freqs"
]

from collections import defaultdict
from typing import List, Tuple

from pythainlp.corpus import get_corpus_path

_FILENAME = "oscar_icu"


def word_freqs() -> List[Tuple[str, int]]:
    """
    Get word frequency from OSCAR Corpus (icu word tokenize)
    """
    word_freqs = []
    _path = get_corpus_path(_FILENAME)
    with open(_path,"r",encoding="utf-8") as f:
        for line in f.readlines():
            word_freq = line.strip().split(",")
            if len(word_freq) >= 2:
                word_freqs.append((word_freq[0], int(word_freq[1])))

    return word_freqs


def unigram_word_freqs() -> defaultdict:
    """
    Get unigram word frequency from OSCAR Corpus (icu word tokenize)
    """
    _path = get_corpus_path(_FILENAME)
    _word_freqs = defaultdict(int)
    with open(_path, "r", encoding="utf-8-sig") as fh:
        _data = [i for i in fh.readlines()]
        del _data[0]
        for i in _data:
            _temp = i.strip().split(",")
            if _temp[0]!=" " and '"' not in _temp[0]:
                _word_freqs[_temp[0]] = int(_temp[-1])
            elif _temp[0]==" ":
                _word_freqs["<s/>"] = int(_temp[-1])

    return _word_freqs
