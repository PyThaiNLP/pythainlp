# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Constants for the Blackboard treebank POS tag set."""

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
            (ESCAPE_TO_CHAR[word], TO_UD[tag])
            if word in keys
            else (word, TO_UD[tag])
            for word, tag in word_tags
        ]
    return word_tags
