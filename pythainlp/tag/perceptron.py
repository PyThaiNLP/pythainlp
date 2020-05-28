# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os
import pickle
from typing import List, Tuple

from pythainlp.corpus import corpus_path
from pythainlp.tag.orchid import tag_signs, tag_to_text

_ORCHID_DATA_FILENAME = "orchid_pt_tagger.pkl"
_PUD_DATA_FILENAME = "ud_thai_pud_pt_tagger.pkl"


def _load_tagger(filename):
    data_filename = os.path.join(corpus_path(), filename)
    with open(data_filename, "rb") as fh:
        model = pickle.load(fh)
    return model


_ORCHID_TAGGER = _load_tagger(_ORCHID_DATA_FILENAME)
_PUD_TAGGER = _load_tagger(_PUD_DATA_FILENAME)


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    :param list words: a list of tokenized words
    :param str corpus: name corpus (orchid or pud)
    :return: returns a list of labels regarding which part of speech it is
    :rtype: list[tuple[str, str]]
    """
    if not words:
        return []

    if corpus == "orchid":
        tagger = _ORCHID_TAGGER
        words = tag_signs(words)
        t2 = tagger.tag(words)
        t = []
        i = 0
        while i < len(t2):
            word = tag_to_text(t2[i][0])
            tag = t2[i][1]
            t.append((word, tag))
            i += 1
    else:  # default, use "pud" as a corpus
        tagger = _PUD_TAGGER
        t = tagger.tag(words)

    return t
