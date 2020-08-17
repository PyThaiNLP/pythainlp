# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech tagger
"""
import json
import os
from typing import List, Tuple

from pythainlp.corpus import corpus_path
from pythainlp.tag.orchid import tag_signs, tag_to_text
from pythainlp.tag.lst20 import (
    _lst20_tagger,
    lst20_tag_signs,
    lst20_tag_to_text,
)

_THAI_POS_ORCHID_FILENAME = "orchid_pos_th.json"
_THAI_POS_ORCHID_PATH = os.path.join(corpus_path(), _THAI_POS_ORCHID_FILENAME)
_THAI_POS_PUD_FILENAME = "ud_thai_pud_unigram_tagger.json"
_THAI_POS_PUD_PATH = os.path.join(corpus_path(), _THAI_POS_PUD_FILENAME)


def _find_tag(words: List[str], dictdata: dict) -> List[Tuple[str, str]]:
    _temp = []
    _word = list(dictdata.keys())
    for word in words:
        if word in _word:
            _temp.append((word, dictdata[word]))
        else:
            _temp.append((word, None))
    return _temp


def _orchid_tagger():
    with open(_THAI_POS_ORCHID_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _pud_tagger():
    with open(_THAI_POS_PUD_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _postag_clean(words, tagger, tag_sign, to_text):
    words = tag_sign(words)
    _t = _find_tag(words, tagger())
    i = 0
    temp = []
    while i < len(_t):
        word = tag_to_text(_t[i][0])
        tag = _t[i][1]
        temp.append((word, tag))
        i += 1

    return temp


def tag(words: List[str], corpus: str) -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    t = []
    if not words:
        return []

    if corpus == "orchid":
        t = _postag_clean(words, _orchid_tagger, tag_signs, tag_to_text)
    elif corpus == "lst20":
        t = _postag_clean(
            words, _lst20_tagger, lst20_tag_signs, lst20_tag_to_text
        )
    else:
        t = _find_tag(words, _pud_tagger())

    return t
