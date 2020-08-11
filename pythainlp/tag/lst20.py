# -*- coding: utf-8 -*-
from typing import List, Tuple
import json

from pythainlp.corpus import get_corpus_path

def get_path(model:str) -> str:
    if model == "perceptron":
        path = get_corpus_path("lst20_pt_tagger")
    elif model == "unigram":
        path = get_corpus_path("lst20_unigram_tagger")
    
    return path


def _lst20_tagger():
    with open(get_path("unigram"), encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _lst20_perceptron():
    return get_path("perceptron")