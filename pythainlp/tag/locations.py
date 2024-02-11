# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Recognizes locations in text
"""

from typing import List, Tuple

from pythainlp.corpus import provinces


def tag_provinces(tokens: List[str]) -> List[Tuple[str, str]]:
    """
    This function recognizes Thailand provinces in text.

    Note that it uses exact match and considers no context.

    :param list[str] tokens: a list of words
    :return: a list of tuples indicating NER for `LOCATION` in IOB format
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
