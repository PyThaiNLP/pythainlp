# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from International Components for Unicode (ICU) dictionary.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus


_THAI_ICU_FILENAME = "icubrk_th.txt"


def thai_icu_words() -> FrozenSet[str]:
    """
    Return a frozenset of words from the Thai dictionary for BreakIterator of the
    International Components for Unicode (ICU).

    :return: :class:`frozenset` containing Thai words.
    :rtype: :class:`frozenset`
    """

    _WORDS = get_corpus(_THAI_ICU_FILENAME, comments=False)

    return _WORDS
