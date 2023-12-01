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
