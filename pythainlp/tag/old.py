# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech Tagger
"""
import json
import os

import dill
import nltk.tag
import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")


def orchid_data():
    template_file = os.path.join(TEMPLATES_DIR, "thaipos.json")
    with open(template_file, "r", encoding="utf-8-sig") as handle:
        model = json.load(handle)
    return model


def pud_data():
    template_file = os.path.join(TEMPLATES_DIR, "ud_thai-pud_unigram_tagger.dill")
    with open(template_file, "rb") as handle:
        model = dill.load(handle)
    return model


def tag(text, corpus):
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('ข้อความ', 'ชนิดคำ')]"""
    if corpus == "orchid":
        tagger = nltk.tag.UnigramTagger(model=orchid_data())
        return tagger.tag(text)

    # default, use "pud" as a corpus
    tagger = pud_data()
    return tagger.tag(text)
