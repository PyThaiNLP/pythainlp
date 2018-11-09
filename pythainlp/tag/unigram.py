# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech Tagger
"""
import json
import os

import dill
import nltk.tag
from pythainlp.corpus import CORPUS_PATH

_THAI_POS_ORCHID_FILENAME = "orchid_pos_th.json"
_THAI_POS_ORCHID_PATH = os.path.join(CORPUS_PATH, _THAI_POS_ORCHID_FILENAME)
_THAI_POS_PUD_FILENAME = "ud_thai_pud_unigram_tagger.dill"
_THAI_POS_PUD_PATH = os.path.join(CORPUS_PATH, _THAI_POS_PUD_FILENAME)


def _orchid_tagger():
    with open(_THAI_POS_ORCHID_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _pud_tagger():
    with open(_THAI_POS_PUD_PATH, "rb") as handle:
        model = dill.load(handle)
    return model


def tag(words, corpus):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    if corpus == "orchid":
        tagger = nltk.tag.UnigramTagger(model=_orchid_tagger())
        return tagger.tag(words)

    # default, use "pud" as a corpus
    tagger = _pud_tagger()
    return tagger.tag(words)
