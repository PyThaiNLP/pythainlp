# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Provides an optional word list from Thai Wikipedia titles.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_WIKIPEDIA_TITLES = None
_WIKIPEDIA_TITLES_FILENAME = "wikipedia_titles.txt"


def wikipedia_titles() -> FrozenSet[str]:
    """
    Return a frozenset of words in the Thai Wikipedia titles corpus.

    The data file is at pythainlp/corpus/wikipedia_titles.txt
    The word list has beed prepared by the code at:
    https://github.com/konbraphat51/Thai_Dictionary_Cleaner

    :return: :class:`frozenset` containing words in Thai Wikipedia titles corpus.
    :rtype: :class:`frozenset`
    """
    global _WIKIPEDIA_TITLES
    if not _WIKIPEDIA_TITLES:
        _WIKIPEDIA_TITLES = get_corpus(_WIKIPEDIA_TITLES_FILENAME)

    return _WIKIPEDIA_TITLES
