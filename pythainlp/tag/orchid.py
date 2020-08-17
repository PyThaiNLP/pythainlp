# -*- coding: utf-8 -*-
"""
Data preprocessing for ORCHID corpus
"""
from typing import List

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


def tag_signs(words: List[str]) -> List[str]:
    """
    Tag signs and symbols with their tags.
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
