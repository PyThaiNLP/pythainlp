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
Provides an optional corpus of Wikipedia titles.
"""
from typing import FrozenSet

from pythainlp.corpus.common import get_corpus

_VOLUBILIS = None
_VOLUBILIS_FILENAME = "volubilis_modified.txt"


def volubilis() -> FrozenSet[str]:
    """
    Return a frozenset of words in the Volubilis corpus.

    The data is in dev/pythainlp/corpus/volubilis_modified.txt
    The corpus has beed cleaned by this repository:
    https://github.com/konbraphat51/Thai_Dictionary_Cleaner

    :return: :class:`frozenset` containing words in the wikipedia titles corpus.
    :rtype: :class:`frozenset`
    """
    global _VOLUBILIS
    if not _VOLUBILIS:
        _VOLUBILIS = get_corpus(_VOLUBILIS_FILENAME)

    return _VOLUBILIS
