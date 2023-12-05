# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2016-2023 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from International Components for Unicode (ICU) dictionary.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_THAI_ICU = None
_THAI_ICU_FILENAME = "thai_icu.txt"


def thai_icu() -> FrozenSet[str]:
    """
    Return a frozenset of words from the International Components for Unicode (ICU) dictionary.

    The data is at pythainlp/corpus/thai_icu.txt
    The word list has beed prepared by the code at:
    https://github.com/unicode-org/icu/blob/main/icu4c/source/data/brkitr/dictionaries/thaidict.txt

    :return: :class:`frozenset` containing words in the Thai ICU dictionary.
    :rtype: :class:`frozenset`
    """
    global _THAI_ICU
    if not _THAI_ICU:
        _THAI_ICU = get_corpus(_THAI_ICU_FILENAME)

    return _THAI_ICU
