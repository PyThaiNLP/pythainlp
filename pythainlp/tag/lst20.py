# -*- coding: utf-8 -*-
from typing import List, Tuple
import json

from pythainlp.corpus import get_corpus_path

LST20_SIGN_TAGS = {" ": "_"}
LST20_SIGN_TEXTS = dict((v, k) for k, v in LST20_SIGN_TAGS.items())


# map from LST20 POS tag to Universal POS tag
# from Wannaphong Phatthiyaphaibun & Korakot Chaovavanich
LST20_TO_UD = {
    "AJ": "ADJ",
    "AV": "ADV",
    "AX": "AUX",
    "CC": "CCONJ",
    "CL": "NOUN",
    "FX": "NOUN",
    "IJ": "INTJ",
    "NN": "NOUN",
    "NU": "NUM",
    "PA": "PART",
    "PR": "PROPN",
    "PS": "ADP",
    "PU": "PUNCT",
    "VV": "VERB",
    "XX": "X",
}


def to_ud(word_tags: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    return [(word_tag[0], LST20_TO_UD[word_tag[1]]) for word_tag in word_tags]


def tag_signs(words: List[str]) -> List[str]:
    """
    Mark signs and symbols with their tags.
    This function is to be used a preprocessing before the actual POS tagging.
    """
    keys = LST20_SIGN_TAGS.keys()
    words = [LST20_SIGN_TAGS[word] if word in keys else word for word in words]
    return words


def tag_to_text(word: str) -> str:
    """
    Return a corresponding text for the word, if found.
    If not found, return the word itself.
    """
    if word in LST20_SIGN_TEXTS.keys():
        word = LST20_SIGN_TEXTS[word]
    return word
