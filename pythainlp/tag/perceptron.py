# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os

import dill
from pythainlp.corpus import CORPUS_PATH


def orchid_data():
    data_filename = os.path.join(CORPUS_PATH, "orchid_pt_tagger.dill")
    with open(data_filename, "rb") as fh:
        model = dill.load(fh)
    return model


def pud_data():
    data_filename = os.path.join(CORPUS_PATH, "ud_thai_pud_pt_tagger.dill")
    with open(data_filename, "rb") as fh:
        model = dill.load(fh)
    return model


def tag(text, corpus="pud"):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if corpus == "orchid":
        tagger = orchid_data()
        return tagger.tag(text)
    else:  # default, use "pud" as a corpus
        tagger = pud_data()
        return tagger.tag(text)
