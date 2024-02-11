# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai Textbook Corpus (TTC) word frequency

Credit: Korakot Chaovavanich
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""

__all__ = ["word_freqs", "unigram_word_freqs"]

from collections import defaultdict
from typing import List, Tuple

from pythainlp.corpus import get_corpus

_FILENAME = "ttc_freq.txt"


def word_freqs() -> List[Tuple[str, int]]:
    """
    Get word frequency from Thai Textbook Corpus (TTC)
    \n(See: `dev/pythainlp/corpus/ttc_freq.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/ttc_freq.txt>`_)
    """
    lines = list(get_corpus(_FILENAME))
    word_freqs = []
    for line in lines:
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            word_freqs.append((word_freq[0], int(word_freq[1])))

    return word_freqs


def unigram_word_freqs() -> defaultdict:
    """
    Get unigram word frequency from Thai Textbook Corpus (TTC)
    """
    lines = list(get_corpus(_FILENAME))
    _word_freqs = defaultdict(int)
    for i in lines:
        _temp = i.strip().split("	")
        if len(_temp) >= 2:
            _word_freqs[_temp[0]] = int(_temp[-1])

    return _word_freqs
