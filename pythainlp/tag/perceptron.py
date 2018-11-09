# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os

import dill
from pythainlp.corpus import CORPUS_PATH

_ORCHID_DATA_FILENAME = "orchid_pt_tagger.dill"
_PUD_DATA_FILENAME = "ud_thai_pud_pt_tagger.dill"


def _load_tagger(filename):
    data_filename = os.path.join(CORPUS_PATH, filename)
    with open(data_filename, "rb") as fh:
        model = dill.load(fh)
    return model


_ORCHID_TAGGER = _load_tagger(_ORCHID_DATA_FILENAME)
_PUD_TAGGER = _load_tagger(_PUD_DATA_FILENAME)


def tag(words, corpus="pud"):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    words = [word.strip() for word in words if word.strip()]

    if corpus == "orchid":
        tagger = _ORCHID_TAGGER
    else:  # default, use "pud" as a corpus
        tagger = _PUD_TAGGER

    return tagger.tag(words)
