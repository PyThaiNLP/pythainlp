# -*- coding: utf-8 -*-
"""
Perceptron part-of-speech tagger
"""
import os
import pickle
from typing import List, Tuple

from pythainlp.corpus import corpus_path, get_corpus_path


_ORCHID_FILENAME = "pos_orchid_perceptron.pkl"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "pos_ud_perceptron.pkl"
_PUD_PATH = os.path.join(corpus_path(), _PUD_FILENAME)

_LST20_TAGGER_NAME = "pos_lst20_perceptron"

_ORCHID_TAGGER = None
_PUD_TAGGER = None
_LST20_TAGGER = None


def _orchid_tagger():
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        with open(_ORCHID_PATH, "rb") as fh:
            _ORCHID_TAGGER = pickle.load(fh)
    return _ORCHID_TAGGER


def _pud_tagger():
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        with open(_PUD_PATH, "rb") as fh:
            _PUD_TAGGER = pickle.load(fh)
    return _PUD_TAGGER


def _lst20_tagger():
    global _LST20_TAGGER
    if not _LST20_TAGGER:
        path = get_corpus_path(_LST20_TAGGER_NAME)
        with open(path, "rb") as fh:
            _LST20_TAGGER = pickle.load(fh)
    return _LST20_TAGGER


# actual tagging work happens here
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

    word_tags = []
    if corpus == "orchid" or corpus == "orchid_ud":
        from pythainlp.tag.orchid import tag_signs, tag_to_text, to_ud

        tagger = _orchid_tagger()
        word_tags = _postag_clean(words, tagger, tag_signs, tag_to_text)
        if corpus == "orchid_ud":
            word_tags = to_ud(word_tags)
    elif corpus == "lst20" or corpus == "lst20_ud":
        from pythainlp.tag.lst20 import tag_signs, tag_to_text, to_ud

        tagger = _lst20_tagger()
        word_tags = _postag_clean(words, tagger, tag_signs, tag_to_text)
        if corpus == "lst20_ud":
            word_tags = to_ud(word_tags)
    else:  # default, use "pud" as a corpus
        tagger = _pud_tagger()
        word_tags = tagger.tag(words)

    return word_tags
