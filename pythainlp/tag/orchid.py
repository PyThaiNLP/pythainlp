# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Data preprocessing for the ORCHID corpus."""

from __future__ import annotations

# defined strings for special characters,
# from Table 4 in ORCHID paper
CHAR_TO_ESCAPE: dict[str, str] = {
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
ESCAPE_TO_CHAR: dict[str, str] = {v: k for k, v in CHAR_TO_ESCAPE.items()}

# map from ORCHID POS tag to Universal POS tag
# from Korakot Chaovavanich
TO_UD: dict[str, str] = {
    "": "",
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
    if w in ("การ", "ความ"):
        return "NOUN"

    return tag


def pre_process(words: list[str]) -> list[str]:
    """
    Convert signs and symbols to their defined strings.

    Use this function as a preprocessing step before POS tagging.

    :param list[str] words: list of words to be converted
    :return: list of words with signs and symbols replaced
    :rtype: list[str]
    """
    keys = CHAR_TO_ESCAPE.keys()
    words = [CHAR_TO_ESCAPE[word] if word in keys else word for word in words]
    return words


def post_process(
    word_tags: list[tuple[str, str]], to_ud: bool = False
) -> list[tuple[str, str]]:
    """
    Convert defined strings back to signs and symbols.

    Use this function as a post-processing step after POS tagging.

    :param list[tuple[str, str]] word_tags: list of (word, POS tag) pairs
    :param bool to_ud: map the POS tags to Universal POS tags
    :return: list of (word, POS tag) pairs with signs and symbols restored
    :rtype: list[tuple[str, str]]
    """
    keys = ESCAPE_TO_CHAR.keys()

    if not to_ud:
        word_tags = [
            (ESCAPE_TO_CHAR[word], tag) if word in keys else (word, tag)
            for word, tag in word_tags
        ]
    else:
        word_tags = [
            (ESCAPE_TO_CHAR[word], ud_exception(word, TO_UD[tag]))
            if word in keys
            else (word, ud_exception(word, TO_UD[tag]))
            for word, tag in word_tags
        ]
    return word_tags
