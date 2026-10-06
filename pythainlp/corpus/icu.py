# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Provide an optional word list from the ICU dictionary.

ICU is International Components for Unicode.
"""

from __future__ import annotations

from pythainlp.corpus.core import get_corpus

_THAI_ICU_FILENAME: str = "icubrk_th.txt"


def thai_icu_words() -> frozenset[str]:
    """
    Return a frozenset of words from the Thai dictionary for ICU BreakIterator.

    ICU is International Components for Unicode.

    :return: frozenset of Thai words
    :rtype: frozenset[str]
    """
    _WORDS = get_corpus(_THAI_ICU_FILENAME, comments=False)

    return _WORDS
