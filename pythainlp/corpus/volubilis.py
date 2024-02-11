# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from the Volubilis dictionary.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_VOLUBILIS_WORDS = None
_VOLUBILIS_FILENAME = "volubilis_words_th.txt"


def thai_volubilis_words() -> FrozenSet[str]:
    """
    Return a frozenset of Thai words from the Volubilis dictionary
    
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
