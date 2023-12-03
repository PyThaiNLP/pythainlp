# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2016-2023 PyThaiNLP Project.
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from Thai Wikipedia titles.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_WIKIPEDIA_TITLES = None
_WIKIPEDIA_TITLES_FILENAME = "wikipedia_titles.txt"


def wikipedia_titles() -> FrozenSet[str]:
    """
    Return a frozenset of words from Thai Wikipedia titles corpus.
    They are mostly nouns and noun phrases,
    including event, organization, people, place, and product names.
    Commonly misspelled words are included intentionally.

    More info:
    https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md

    :return: :class:`frozenset` containing words in Thai Wikipedia titles.
    :rtype: :class:`frozenset`
    """
    global _WIKIPEDIA_TITLES
    if not _WIKIPEDIA_TITLES:
        _WIKIPEDIA_TITLES = get_corpus(_WIKIPEDIA_TITLES_FILENAME)

    return _WIKIPEDIA_TITLES
