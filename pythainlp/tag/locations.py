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
Recognizes locations in text
"""

from typing import List, Tuple

from pythainlp.corpus import provinces


def tag_provinces(tokens: List[str]) -> List[Tuple[str, str]]:
    """
    This function recognize Thailand provinces in text.

    Note that it uses exact match and considers no context.

    :param list[str] tokens: a list of words
    :reutrn: a list of tuple indicating NER for `LOCATION` in IOB format
    :rtype: list[tuple[str, str]]

    :Example:
    ::

        from pythainlp.tag import tag_provinces

        text = ['หนองคาย', 'น่าอยู่']
        tag_provinces(text)
        # output: [('หนองคาย', 'B-LOCATION'), ('น่าอยู่', 'O')]
    """
    province_list = provinces()
    output = [
        (token, "B-LOCATION") if token in province_list else (token, "O")
        for token in tokens
    ]
    return output
