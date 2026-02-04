# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Provides an optional word list from International Components for Unicode (ICU) dictionary."""

from __future__ import annotations

from pythainlp.corpus.core import get_corpus

_THAI_ICU_FILENAME: str = "icubrk_th.txt"


def thai_icu_words() -> frozenset[str]:
    """Return a frozenset of words from the Thai dictionary for BreakIterator of the
    International Components for Unicode (ICU).

    :return: :class:`frozenset` containing Thai words.
    :rtype: :class:`frozenset`
    """
    _WORDS = get_corpus(_THAI_ICU_FILENAME, comments=False)

    return _WORDS
