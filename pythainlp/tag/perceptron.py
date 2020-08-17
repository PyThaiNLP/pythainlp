# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os
import pickle
from typing import List, Tuple

from pythainlp.corpus import corpus_path
from pythainlp.tag.lst20 import (
    _lst20_perceptron,
    lst20_tag_signs,
    lst20_tag_to_text,
)
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


def _postag_clean(words: List[str], tagger, tag_signs, to_text):
    words = tag_signs(words)
    word_tags = tagger.tag(words)

    return [(to_text(word_tag[0]), word_tag[1]) for word_tag in word_tags]


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    :param list words: a list of tokenized words
    :param str corpus: name corpus (orchid or pud)
    :return: returns a list of labels regarding which part of speech it is
    :rtype: list[tuple[str, str]]
    """
    if not words:
        return []

    t = []
    if corpus == "orchid":
        tagger = _ORCHID_TAGGER
        t = _postag_clean(words, tagger, tag_signs, tag_to_text)
    elif corpus == "lst20":
        tagger = _load_tagger(_lst20_perceptron())
        t = _postag_clean(words, tagger, lst20_tag_signs, lst20_tag_to_text)
    else:  # default, use "pud" as a corpus
        tagger = _PUD_TAGGER
        t = tagger.tag(words)

    return t
