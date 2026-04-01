# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai National Corpus word frequency"""

from __future__ import annotations

__all__: list[str] = [
    "bigram_word_freqs",
    "trigram_word_freqs",
    "unigram_word_freqs",
    "word_freqs",
]

from collections import defaultdict

from pythainlp.corpus import get_corpus, get_corpus_path

_UNIGRAM_FILENAME: str = "tnc_freq.txt"
_BIGRAM_CORPUS_NAME: str = "tnc_bigram_word_freqs"
_TRIGRAM_CORPUS_NAME: str = "tnc_trigram_word_freqs"


def word_freqs() -> list[tuple[str, int]]:
    """Get word frequency from Thai National Corpus (TNC).

    (See: `dev/pythainlp/corpus/tnc_freq.txt
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/tnc_freq.txt>`_)

    :See Also:
        * Korakot Chaovavanich.
          https://www.facebook.com/groups/thainlp/posts/434330506948445
    """
    freqs: list[tuple[str, int]] = []
    for line in get_corpus(_UNIGRAM_FILENAME):
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            freqs.append((word_freq[0], int(word_freq[1])))

    return freqs


def unigram_word_freqs() -> dict[str, int]:
    """Get unigram word frequency from Thai National Corpus (TNC)"""
    freqs: dict[str, int] = defaultdict(int)
    for line in get_corpus(_UNIGRAM_FILENAME):
        _temp = line.strip().split("	")
        if len(_temp) >= 2:
            freqs[_temp[0]] = int(_temp[-1])

    return freqs


def bigram_word_freqs() -> dict[tuple[str, str], int]:
    """Get bigram word frequency from Thai National Corpus (TNC)"""
    freqs: dict[tuple[str, str], int] = defaultdict(int)
    path = get_corpus_path(_BIGRAM_CORPUS_NAME)
    if not path:
        return freqs
    path = str(path)

    try:
        with open(path, encoding="utf-8-sig") as fh:
            for line in fh:
                temp = line.strip().split("	")
                if len(temp) >= 3:
                    freqs[(temp[0], temp[1])] = int(temp[-1])
    except (IOError, OSError):
        pass

    return freqs


def trigram_word_freqs() -> dict[tuple[str, str, str], int]:
    """Get trigram word frequency from Thai National Corpus (TNC)"""
    freqs: dict[tuple[str, str, str], int] = defaultdict(int)
    path = get_corpus_path(_TRIGRAM_CORPUS_NAME)
    if not path:
        return freqs
    path = str(path)

    try:
        with open(path, encoding="utf-8-sig") as fh:
            for line in fh:
                temp = line.strip().split("	")
                if len(temp) >= 4:
                    freqs[(temp[0], temp[1], temp[2])] = int(temp[-1])
    except (IOError, OSError):
        pass

    return freqs
