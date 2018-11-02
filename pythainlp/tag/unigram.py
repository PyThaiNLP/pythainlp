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
_THAI_POS_PUD_FILENAME = "ud_thai-pud_unigram_tagger.dill"
_THAI_POS_PUD_PATH = os.path.join(CORPUS_PATH, _THAI_POS_PUD_FILENAME)


def orchid_data():
    with open(_THAI_POS_ORCHID_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def pud_data():
    with open(_THAI_POS_PUD_PATH, "rb") as handle:
        model = dill.load(handle)
    return model


def tag(text, corpus):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if corpus == "orchid":
        tagger = nltk.tag.UnigramTagger(model=orchid_data())
        return tagger.tag(text)

    # default, use "pud" as a corpus
    tagger = pud_data()
    return tagger.tag(text)
