# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech tagger
"""
import json
import os
from typing import List, Tuple

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import lst20, orchid


_ORCHID_FILENAME = "pos_orchid_unigram.json"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "pos_ud_unigram.json"
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


def _tag(
    words: List[str], tagger, pre_process, post_process, to_ud: bool = False
):
    words = pre_process(words)
    word_tags = _find_tag(words, tagger())
    word_tags = post_process(word_tags, to_ud)
    return word_tags


def tag(words: List[str], corpus: str) -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    to_ud = False
    if corpus[-3:] == "_ud":
        to_ud = True

    word_tags = []
    if corpus == "orchid" or corpus == "orchid_ud":
        word_tags = _tag(
            words,
            _orchid_tagger,
            orchid.pre_process,
            orchid.post_process,
            to_ud,
        )
    elif corpus == "lst20" or corpus == "lst20_ud":
        word_tags = _tag(
            words, _lst20_tagger, lst20.pre_process, lst20.post_process, to_ud
        )
    else:  # default, use "pud" as a corpus
        word_tags = _find_tag(words, _pud_tagger())

    return word_tags
