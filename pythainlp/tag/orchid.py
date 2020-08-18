# -*- coding: utf-8 -*-
"""
Data preprocessing for ORCHID corpus
"""
from typing import List, Tuple

# ORCHID part-of-speech tags
ORCHID_SIGN_TAGS = {
    " ": "<space>",
    "+": "<plus>",
    "-": "<minus>",
    "=": "<equal>",
    ",": "<comma>",
    "$": "<dollar>",
    ".": "<full_stop>",
    "(": "<left_parenthesis>",
    ")": "<right_parenthesis>",
    '"': "<quotation>",
    "@": "<at_mark>",
    "&": "<ampersand>",
    "{": "<left_curly_bracket>",
    "^": "<circumflex_accent>",
    "?": "<question_mark>",
    "<": "<less_than>",
    ">": "<greater_than>",
    "!": "<exclamation>",
    "’": "<apostrophe>",
    ":": "<colon>",
    "*": "<asterisk>",
    ";": "<semi_colon>",
    "/": "<slash>",
}
ORCHID_SIGN_TEXTS = dict((v, k) for k, v in ORCHID_SIGN_TAGS.items())

# map from ORCHID POS tag to Universal POS tag
# from Korakot Chaovavanich
ORCHID_TO_UD = {
    # NOUN
    "NOUN": "NOUN",
    "NCMN": "NOUN",
    "NTTL": "NOUN",
    "CNIT": "NOUN",
    "CLTV": "NOUN",
    "CMTR": "NOUN",
    "CFQC": "NOUN",
    "CVBL": "NOUN",
    # VERB
    "VACT": "VERB",
    "VSTA": "VERB",
    # PROPN
    "PROPN": "PROPN",
    "NPRP": "PROPN",
    # ADJ
    "ADJ": "ADJ",
    "NONM": "ADJ",
    "VATT": "ADJ",
    "DONM": "ADJ",
    # ADV
    "ADV": "ADV",
    "ADVN": "ADV",
    "ADVI": "ADV",
    "ADVP": "ADV",
    "ADVS": "ADV",
    # INT
    "INT": "INTJ",
    # PRON
    "PRON": "PRON",
    "PPRS": "PRON",
    "PDMN": "PRON",
    "PNTR": "PRON",
    # DET
    "DET": "DET",
    "DDAN": "DET",
    "DDAC": "DET",
    "DDBQ": "DET",
    "DDAQ": "DET",
    "DIAC": "DET",
    "DIBQ": "DET",
    "DIAQ": "DET",
    # NUM
    "NUM": "NUM",
    "NCNM": "NUM",
    "NLBL": "NUM",
    "DCNM": "NUM",
    # AUX
    "AUX": "AUX",
    "XVBM": "AUX",
    "XVAM": "AUX",
    "XVMM": "AUX",
    "XVBB": "AUX",
    "XVAE": "AUX",
    # ADP
    "ADP": "ADP",
    "RPRE": "ADP",
    # CCONJ
    "CCONJ": "CCONJ",
    "JCRG": "CCONJ",
    # SCONJ
    "SCONJ": "SCONJ",
    "PREL": "SCONJ",
    "JSBR": "SCONJ",
    "JCMP": "SCONJ",
    # PART
    "PART": "PART",
    "FIXN": "PART",
    "FIXV": "PART",
    "EAFF": "PART",
    "EITT": "PART",
    "AITT": "PART",
    "NEG": "PART",
    # PUNCT
    "PUNCT": "PUNCT",
    "PUNC": "PUNCT",
}


def ud_exception(w: str, tag: str) -> str:
    if w == "การ" or w == "ความ":
        return "NOUN"

    return tag


def to_ud(word_tags: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    return [
        (word_tag[0], ud_exception(word_tag[0], ORCHID_TO_UD[word_tag[1]]))
        for word_tag in word_tags
    ]


def tag_signs(words: List[str]) -> List[str]:
    """
    Mark signs and symbols with their tags.
    This function is to be used a preprocessing before the actual POS tagging.
    """
    keys = ORCHID_SIGN_TAGS.keys()
    words = [
        ORCHID_SIGN_TAGS[word] if word in keys else word for word in words
    ]
    return words


def tag_to_text(word: str) -> str:
    """
    Return a corresponding text for the word, if found.
    If not found, return the word itself.
    """
    if word in ORCHID_SIGN_TEXTS.keys():
        word = ORCHID_SIGN_TEXTS[word]
    return word
