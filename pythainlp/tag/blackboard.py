# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

# defined strings for special characters
CHAR_TO_ESCAPE: dict[str, str] = {" ": "_"}
ESCAPE_TO_CHAR: dict[str, str] = {v: k for k, v in CHAR_TO_ESCAPE.items()}


# map from Blackboard treebank POS tag to Universal POS tag
# from Wannaphong Phatthiyaphaibun & Korakot Chaovavanich
TO_UD: dict[str, str] = {
    "": "",
    "AJ": "ADJ",
    "AV": "ADV",
    "AX": "AUX",
    "CC": "CCONJ",
    "CL": "NOUN",
    "FX": "NOUN",
    "IJ": "INTJ",
    "NG": "PART",
    "NN": "NOUN",
    "NU": "NUM",
    "PA": "PART",
    "PR": "PROPN",
    "PS": "ADP",
    "PU": "PUNCT",
    "VV": "VERB",
    "XX": "X",
}


def pre_process(words: list[str]) -> list[str]:
    """Convert signs and symbols with their defined strings.
    This function is to be used as a preprocessing step,
    before the actual POS tagging.
    """
    keys = CHAR_TO_ESCAPE.keys()
    words = [CHAR_TO_ESCAPE[word] if word in keys else word for word in words]
    return words


def post_process(
    word_tags: list[tuple[str, str]], to_ud: bool = False
) -> list[tuple[str, str]]:
    """Convert defined strings back to corresponding signs and symbols.
    This function is to be used as a post-processing step,
    after the POS tagging.
    """
    keys = ESCAPE_TO_CHAR.keys()

    if not to_ud:
        word_tags = [
            (ESCAPE_TO_CHAR[word], tag) if word in keys else (word, tag)
            for word, tag in word_tags
        ]
    else:
        word_tags = [
            (ESCAPE_TO_CHAR[word], TO_UD[tag])
            if word in keys
            else (word, TO_UD[tag])
            for word, tag in word_tags
        ]
    return word_tags
