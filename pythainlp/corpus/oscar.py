# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai unigram word frequency from OSCAR Corpus (words tokenized using ICU)

Credit: Korakot Chaovavanich
https://web.facebook.com/groups/colab.thailand/permalink/1524070061101680/
"""

__all__ = ["word_freqs", "unigram_word_freqs"]

from collections import defaultdict
from typing import List, Tuple

from pythainlp.corpus import get_corpus_path

_FILENAME = "oscar_icu"


def word_freqs() -> List[Tuple[str, int]]:
    """
    Get word frequency from OSCAR Corpus (words tokenized using ICU)
    """
    word_freqs = []
    _path = get_corpus_path(_FILENAME)
    with open(_path, "r", encoding="utf-8-sig") as f:
        _data = list(f.readlines())
        del _data[0]
        for line in _data:
            _temp = line.strip().split(",")
            if len(_temp) >= 2:
                if _temp[0] != " " and '"' not in _temp[0]:
                    word_freqs.append((_temp[0], int(_temp[1])))
                elif _temp[0] == " ":
                    word_freqs.append(("<s/>", int(_temp[1])))

    return word_freqs


def unigram_word_freqs() -> defaultdict:
    """
    Get unigram word frequency from OSCAR Corpus (words tokenized using ICU)
    """
    _path = get_corpus_path(_FILENAME)
    _word_freqs = defaultdict(int)
    with open(_path, "r", encoding="utf-8-sig") as fh:
        _data = list(fh.readlines())
        del _data[0]
        for i in _data:
            _temp = i.strip().split(",")
            if _temp[0] != " " and '"' not in _temp[0]:
                _word_freqs[_temp[0]] = int(_temp[-1])
            elif _temp[0] == " ":
                _word_freqs["<s/>"] = int(_temp[-1])

    return _word_freqs
