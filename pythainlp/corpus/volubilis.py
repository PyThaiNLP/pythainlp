# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2016-2023 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from the Volubilis dictionary.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_VOLUBILIS = None
_VOLUBILIS_FILENAME = "volubilis_modified.txt"


def volubilis() -> FrozenSet[str]:
    """
    Return a frozenset of words from the Volubilis dictionary.

    The data is at pythainlp/corpus/volubilis_modified.txt
    The word list has beed prepared by the code at:
    https://github.com/konbraphat51/Thai_Dictionary_Cleaner
    Based Volubilis dictionary 23.1 (March 2023):
    https://belisan-volubilis.blogspot.com/

    :return: :class:`frozenset` containing words in the Volubilis dictionary.
    :rtype: :class:`frozenset`
    """
    global _VOLUBILIS
    if not _VOLUBILIS:
        _VOLUBILIS = get_corpus(_VOLUBILIS_FILENAME)

    return _VOLUBILIS
