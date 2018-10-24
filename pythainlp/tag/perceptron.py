# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os

import dill
import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")


def orchid_data():
    template_file = os.path.join(TEMPLATES_DIR, "pt_tagger_1.dill")
    with open(template_file, "rb") as handle:
        model = dill.load(handle)
    return model


def pud_data():
    template_file = os.path.join(TEMPLATES_DIR, "ud_thai-pud_pt_tagger.dill")
    with open(template_file, "rb") as handle:
        model = dill.load(handle)
    return model


def tag(text, corpus="pud"):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
    if corpus == "orchid":
        tagger = orchid_data()
        return tagger.tag(text)
    else:  # default, use "pud" as a corpus
        tagger = pud_data()
        return tagger.tag(text)
