# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenize text into Enhanced Thai Character Clusters (ETCCs).

This Python implementation is by Wannaphong Phatthiyaphaibun.
It relies on a dictionary of ETCCs created from ``etcc.txt``
in ``pythainlp/corpus``.

Notebook:
https://colab.research.google.com/drive/1UTQgxxMRxOr9Jp1B1jcq1frBNvorhtBQ

:See Also:

Jeeragone Inrut, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and
Para Limmaneepraserth. "Thai word segmentation using combination of forward
and backward longest matching techniques." In International Symposium on
Communications and Information Technology (ISCIT), pp. 37-40. 2001.
"""

from __future__ import annotations

import re
from functools import lru_cache

from pythainlp import thai_follow_vowels
from pythainlp.corpus import get_corpus
from pythainlp.tokenize import Tokenizer


@lru_cache
def _cut_etcc() -> Tokenizer:
    """Return the ETCC tokenizer, loaded lazily and cached."""
    return Tokenizer(get_corpus("etcc.txt"), engine="longest")


_PAT_ENDING_CHAR: str = f"[{thai_follow_vowels}ๆฯ]"
_RE_ENDING_CHAR: re.Pattern[str] = re.compile(_PAT_ENDING_CHAR)


def _cut_subword(tokens: list[str]) -> list[str]:
    len_tokens = len(tokens)
    i = 0
    while True:
        if i == len_tokens:
            break
        if _RE_ENDING_CHAR.search(tokens[i]) and i > 0 and len(tokens[i]) == 1:
            tokens[i - 1] += tokens[i]
            del tokens[i]
            len_tokens -= 1
        i += 1
    return tokens


def segment(text: str) -> list[str]:
    """
    Tokenize text into ETCCs.

    An Enhanced Thai Character Cluster (ETCC) is a kind of subword unit.
    Inrut, Jeeragone, Patiroop Yuanghirun, Sarayut Paludkong,
    Supot Nitsuwat, and Para Limmaneepraserth presented the concept in
    "Thai word segmentation using combination of forward and backward
    longest matching techniques." In International Symposium on
    Communications and Information Technology (ISCIT), pp. 37-40. 2001.

    :param str text: text to be tokenized
    :return: list of character clusters
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    return _cut_subword(_cut_etcc().word_tokenize(text))
