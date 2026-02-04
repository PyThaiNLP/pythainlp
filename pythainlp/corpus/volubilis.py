# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Provides an optional word list from the Volubilis dictionary."""

from __future__ import annotations

from typing import Optional

from pythainlp.corpus.core import get_corpus

_VOLUBILIS_WORDS: Optional[frozenset[str]] = None
_VOLUBILIS_FILENAME: str = "volubilis_words_th.txt"


def thai_volubilis_words() -> frozenset[str]:
    """Return a frozenset of Thai words from the Volubilis dictionary

    See: `dev/pythainlp/corpus/volubilis_words_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/volubilis_words_th.txt>`_

    More info:
    https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md

    :return: :class:`frozenset` containing Thai words.
    :rtype: :class:`frozenset`
    """
    global _VOLUBILIS_WORDS
    if not _VOLUBILIS_WORDS:
        _VOLUBILIS_WORDS = get_corpus(_VOLUBILIS_FILENAME, comments=False)

    return _VOLUBILIS_WORDS
