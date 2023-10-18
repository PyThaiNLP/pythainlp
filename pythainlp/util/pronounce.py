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
from typing import List

from pythainlp.corpus import thai_words
from pythainlp.tokenize import syllable_tokenize
from pythainlp.khavee import KhaveeVerifier


kv = KhaveeVerifier()
all_thai_words_dict = [
    i for i in list(thai_words()) if len(syllable_tokenize(i)) == 1
]


def rhyme(word: str) -> List[str]:
    """
    Find Thai rhyme

    :param str word: A Thai word
    :return: All list Thai rhyme words
    :rtype: List[str]

    :Example:
    ::
        from pythainlp.util import rhyme

        print(rhyme("จีบ"))
        # output: ['กลีบ', 'กีบ', 'ครีบ', ...]
    """
    list_sumpus = []
    for i in all_thai_words_dict:
        if kv.is_sumpus(word, i) and i != word:
            list_sumpus.append(i)
    return sorted(list_sumpus)
