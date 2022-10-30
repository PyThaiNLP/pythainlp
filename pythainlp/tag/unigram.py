# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech tagger
"""
import json
import os
from typing import List, Tuple
import warnings

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import lst20, orchid
from pythainlp.util.messages import deprecation_message

_ORCHID_FILENAME = "pos_orchid_unigram.json"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "pos_ud_unigram-v0.2.json"
_PUD_PATH = os.path.join(corpus_path(), _PUD_FILENAME)

_LST20_TAGGER_NAME = "pos_lst20_unigram"


_ORCHID_TAGGER = None
_PUD_TAGGER = None
_LST20_TAGGER = None


def _orchid_tagger():
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        with open(_ORCHID_PATH, encoding="utf-8-sig") as fh:
            _ORCHID_TAGGER = json.load(fh)
    return _ORCHID_TAGGER


def _pud_tagger():
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        with open(_PUD_PATH, encoding="utf-8-sig") as fh:
            _PUD_TAGGER = json.load(fh)
    return _PUD_TAGGER


def _lst20_tagger():
    global _LST20_TAGGER
    warnings.warn(
        """
    LST20 corpus are free for research and open source only.\n
    If you want to use in Commercial use, please contract NECTEC.\n
    https://www.facebook.com/dancearmy/posts/10157641945708284
    """
    )
    if not _LST20_TAGGER:
        path = get_corpus_path(_LST20_TAGGER_NAME)
        with open(path, encoding="utf-8-sig") as fh:
            _LST20_TAGGER = json.load(fh)
    return _LST20_TAGGER


def _find_tag(
    words: List[str], dictdata: dict, default_tag: str = ""
) -> List[Tuple[str, str]]:
    keys = list(dictdata.keys())
    return [
        (word, dictdata[word]) if word in keys else (word, default_tag)
        for word in words
    ]


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
        word_tags = _find_tag(words, _orchid_tagger())
        word_tags = orchid.post_process(word_tags, to_ud)
    elif corpus == "lst20" or corpus == "lst20_ud":
        dep_msg = deprecation_message(
            [("corpus", "lst20"), ("corpus", "lst20_ud")],
            "function `unigram.tag`",
            "4.0.0",
        )
        warnings.warn(dep_msg, DeprecationWarning, stacklevel=2)
        words = lst20.pre_process(words)
        word_tags = _find_tag(words, _lst20_tagger())
        word_tags = lst20.post_process(word_tags, to_ud)
    else:  # default, use "pud" as a corpus
        word_tags = _find_tag(words, _pud_tagger())

    return word_tags
