# -*- coding: utf-8 -*-
"""
Perceptron part-of-speech tagger
"""
import os
import pickle
from typing import List, Tuple

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import PerceptronTagger, lst20, orchid

_ORCHID_FILENAME = "pos_orchid_perceptron.json"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "pos_ud_perceptron.json"
_PUD_PATH = os.path.join(corpus_path(), _PUD_FILENAME)

_LST20_TAGGER_NAME = "pos_lst20_perceptron-v0.2.3.json"
_LST20_TAGGERD_PATH = os.path.join(corpus_path(), _LST20_TAGGER_NAME)

_ORCHID_TAGGER = None
_PUD_TAGGER = None
_LST20_TAGGER = None


def _orchid_tagger():
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        _ORCHID_TAGGER = PerceptronTagger(path=_ORCHID_PATH)
    return _ORCHID_TAGGER


def _pud_tagger():
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        _PUD_TAGGER = PerceptronTagger(path=_PUD_PATH)
    return _PUD_TAGGER


def _lst20_tagger():
    global _LST20_TAGGER
    if not _LST20_TAGGER:
        _LST20_TAGGER = PerceptronTagger(path=_LST20_TAGGERD_PATH)
    return _LST20_TAGGER


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    :param list words: a list of tokenized words
    :param str corpus: corpus name (orchid, pud, or lst20)
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    """
    if not words:
        return []

    to_ud = False
    if corpus[-3:] == "_ud":
        to_ud = True

    word_tags = []
    if corpus == "orchid" or corpus == "orchid_ud":
        words = orchid.pre_process(words)
        word_tags = _orchid_tagger().tag(words)
        word_tags = orchid.post_process(word_tags, to_ud)
    elif corpus == "lst20" or corpus == "lst20_ud":
        words = lst20.pre_process(words)
        word_tags = _lst20_tagger().tag(words)
        word_tags = lst20.post_process(word_tags, to_ud)
    else:  # default, use "pud" as a corpus
        tagger = _pud_tagger()
        word_tags = tagger.tag(words)

    return word_tags
