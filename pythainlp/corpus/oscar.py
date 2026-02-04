# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai unigram word frequency from OSCAR Corpus (words tokenized using ICU)

Credit: Korakot Chaovavanich
https://web.facebook.com/groups/colab.thailand/permalink/1524070061101680/
"""

from __future__ import annotations

__all__: list[str] = ["word_freqs", "unigram_word_freqs"]

from collections import defaultdict

from pythainlp.corpus import get_corpus_path

_OSCAR_FILENAME: str = "oscar_icu"


def word_freqs() -> list[tuple[str, int]]:
    """Get word frequency from OSCAR Corpus (words tokenized using ICU)"""
    freqs: list[tuple[str, int]] = []
    path = get_corpus_path(_OSCAR_FILENAME)
    if not path:
        return freqs
    path = str(path)

    with open(path, encoding="utf-8-sig") as f:
        next(f)  # Skip header line
        for line in f:
            temp = line.strip().split(",")
            if len(temp) >= 2:
                if temp[0] != " " and '"' not in temp[0]:
                    freqs.append((temp[0], int(temp[1])))
                elif temp[0] == " ":
                    freqs.append(("<s/>", int(temp[1])))

    return freqs


def unigram_word_freqs() -> dict[str, int]:
    """Get unigram word frequency from OSCAR Corpus (words tokenized using ICU)"""
    freqs: dict[str, int] = defaultdict(int)
    path = get_corpus_path(_OSCAR_FILENAME)
    if not path:
        return freqs
    path = str(path)

    with open(path, encoding="utf-8-sig") as fh:
        next(fh)  # Skip header line
        for line in fh:
            temp = line.strip().split(",")
            if temp[0] != " " and '"' not in temp[0]:
                freqs[temp[0]] = int(temp[-1])
            elif temp[0] == " ":
                freqs["<s/>"] = int(temp[-1])

    return freqs
