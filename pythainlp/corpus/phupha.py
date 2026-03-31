# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Phupha: Thai Word Frequency Dataset

Phupha is a Thai Word Frequency Dataset from Common Crawl Corpus.

Dataset:
    Phatthiyaphaibun, W. (2026). Phupha: Thai Word Frequency Dataset
    [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18490474

License:
    Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)
"""

from __future__ import annotations

__all__: list[str] = [
    "word_freqs",
    "unigram_word_freqs",
]

from collections import defaultdict

from pythainlp.corpus import get_corpus

_UNIGRAM_FILENAME: str = "phupha_word_freqs.txt"


def word_freqs() -> list[tuple[str, int]]:
    """Get word frequency from Phupha dataset

    Phupha is a Thai Word Frequency Dataset from Common Crawl Corpus.

    :return: List of tuples (word, frequency)
    :rtype: list[tuple[str, int]]

    :Example:

        >>> from pythainlp.corpus import phupha  # doctest: +SKIP
        >>> freqs = phupha.word_freqs()  # doctest: +SKIP
        >>> print(freqs[:5])  # doctest: +SKIP
        [('น', 1119315948), ('ร', 1066483406), ...]

    **Dataset Citation:**

    Phatthiyaphaibun, W. (2026). *Phupha: Thai Word Frequency Dataset*
    [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18490474
    """
    freqs: list[tuple[str, int]] = []
    for line in get_corpus(_UNIGRAM_FILENAME):
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            freqs.append((word_freq[0], int(word_freq[1])))

    return freqs


def unigram_word_freqs() -> dict[str, int]:
    """Get unigram word frequency from Phupha dataset

    Phupha is a Thai Word Frequency Dataset from Common Crawl Corpus.

    :return: Dictionary mapping words to their frequencies
    :rtype: dict[str, int]

    :Example:

        >>> from pythainlp.corpus import phupha  # doctest: +SKIP
        >>> freqs = phupha.unigram_word_freqs()  # doctest: +SKIP
        >>> freqs.get("ไทย", 0)  # doctest: +SKIP

    **Dataset Citation:**

    Phatthiyaphaibun, W. (2026). *Phupha: Thai Word Frequency Dataset*
    [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18490474
    """
    freqs: dict[str, int] = defaultdict(int)
    for line in get_corpus(_UNIGRAM_FILENAME):
        _temp = line.strip().split("\t")
        if len(_temp) >= 2:
            freqs[_temp[0]] = int(_temp[-1])

    return freqs
