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

LST20_SIGN_TAGS = {
    " ": "_"
}
LST20_SIGN_TEXTS = dict((v, k) for k, v in LST20_SIGN_TAGS.items())


def lst20_tag_signs(words: List[str]) -> List[str]:
    """
    Tag signs and symbols with their tags.
    This function is to be used a preprocessing before the actual POS tagging.
    """
    i = 0
    while i < len(words):
        if words[i] in LST20_SIGN_TEXTS.keys():
            words[i] = LST20_SIGN_TEXTS[words[i]]
        i += 1
    return words


def lst20_tag_to_text(word: str) -> str:
    """
    Return a corresponding text for the word, if found.
    If not found, return the word itself.
    """
    if word in LST20_SIGN_TEXTS.keys():
        word = LST20_SIGN_TEXTS[word]
    return word


def _lst20_tagger():
    with open(get_path("unigram"), encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _lst20_perceptron():
    return get_path("perceptron")