# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai Textbook Corpus (TTC) word frequency.

Credit: Korakot Chaovavanich
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""

from __future__ import annotations

__all__: list[str] = ["unigram_word_freqs", "word_freqs"]

from collections import defaultdict

from pythainlp.corpus import get_corpus

_UNIGRAM_FILENAME: str = "ttc_freq.txt"


def word_freqs() -> list[tuple[str, int]]:
    """
    Get word frequency from the Thai Textbook Corpus (TTC).

    See `dev/pythainlp/corpus/ttc_freq.txt
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/ttc_freq.txt>`_.

    :return: list of tuples of word and frequency
    :rtype: list[tuple[str, int]]
    """
    freqs: list[tuple[str, int]] = []
    for line in get_corpus(_UNIGRAM_FILENAME):
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            freqs.append((word_freq[0], int(word_freq[1])))

    return freqs


def unigram_word_freqs() -> dict[str, int]:
    """
    Get unigram word frequency from the Thai Textbook Corpus (TTC).

    :return: dict mapping words to their frequencies
    :rtype: dict[str, int]
    """
    freqs: dict[str, int] = defaultdict(int)

    for line in get_corpus(_UNIGRAM_FILENAME):
        temp = line.strip().split("	")
        if len(temp) >= 2:
            freqs[temp[0]] = int(temp[-1])

    return freqs
