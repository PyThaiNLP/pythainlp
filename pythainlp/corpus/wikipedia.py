# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Provides an optional word list from Thai Wikipedia titles.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_WIKIPEDIA_TITLES = None
_WIKIPEDIA_TITLES_FILENAME = "wikipedia_titles_th.txt"


def thai_wikipedia_titles() -> FrozenSet[str]:
    """
    Return a frozenset of words from Thai Wikipedia titles corpus.
    They are mostly nouns and noun phrases,
    including event, organization, people, place, and product names.
    Commonly misspelled words are included intentionally.

    See: `dev/pythainlp/corpus/wikipedia_titles_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/wikipedia_titles_th.txt>`_

    More info:
    https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md

    :return: :class:`frozenset` containing Thai words.
    :rtype: :class:`frozenset`
    """
    global _WIKIPEDIA_TITLES
    if not _WIKIPEDIA_TITLES:
        _WIKIPEDIA_TITLES = get_corpus(_WIKIPEDIA_TITLES_FILENAME, comments=False)

    return _WIKIPEDIA_TITLES
