# -*- coding: utf-8 -*-
"""
Perceptron Part-Of-Speech tagger
"""
import os
from typing import List, Tuple

import dill
from pythainlp.corpus import corpus_path
from .orchid_preprocessing import orchid_preprocessing, orchid_tag_to_text

_ORCHID_DATA_FILENAME = "orchid_pt_tagger.dill"
_PUD_DATA_FILENAME = "ud_thai_pud_pt_tagger.dill"


def _load_tagger(filename):
    data_filename = os.path.join(corpus_path(), filename)
    with open(data_filename, "rb") as fh:
        model = dill.load(fh)
    return model


_ORCHID_TAGGER = _load_tagger(_ORCHID_DATA_FILENAME)
_PUD_TAGGER = _load_tagger(_PUD_DATA_FILENAME)


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    if corpus == "orchid":
        tagger = _ORCHID_TAGGER
        words = orchid_preprocessing(words)
        t2 = tagger.tag(words)
        t = []
        i = 0
        while i < len(t2):
            word = orchid_tag_to_text(t2[i][0])
            tag = t2[i][1]
            t.append((word, tag))
            i += 1
    else:  # default, use "pud" as a corpus
        tagger = _PUD_TAGGER
        t = tagger.tag(words)

    return t
