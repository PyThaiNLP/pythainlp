# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai collation (sorted according to Thai dictionary order)
Simple implementation using regular expressions
"""
import re
from typing import Iterable, List

_RE_TONE = re.compile(r"[็-์]")
_RE_LV_C = re.compile(r"([เ-ไ])([ก-ฮ])")


def _thkey(word: str) -> str:
    cv = _RE_TONE.sub("", word)  # remove tone
    cv = _RE_LV_C.sub("\\2\\1", cv)  # switch lead vowel
    tone = _RE_TONE.sub(" ", word)  # just tone
    return cv + tone


def collate(data: Iterable, reverse: bool = False) -> List[str]:
    """
    This function sorts strings (almost) according to Thai dictionary.

    Important notes: this implementation ignores tone marks and symbols

    :param data: a list of words to be sorted
    :type data: Iterable
    :param reverse: If `reverse` is set to **True** the result will be
                         sorted in descending order. Otherwise, the result
                         will be sorted in ascending order, defaults to False
    :type reverse: bool, optional

    :return: a list of strings, sorted alphabetically, (almost) according to
             Thai dictionary
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util import collate

        collate(['ไก่', 'เกิด', 'กาล', 'เป็ด', 'หมู', 'วัว', 'วันที่'])
        # output: ['กาล', 'เกิด', 'ไก่', 'เป็ด', 'วันที่', 'วัว', 'หมู']

        collate(['ไก่', 'เกิด', 'กาล', 'เป็ด', 'หมู', 'วัว', 'วันที่'], \\
            reverse=True)
        # output: ['หมู', 'วัว', 'วันที่', 'เป็ด', 'ไก่', 'เกิด', 'กาล']
    """
    return sorted(data, key=_thkey, reverse=reverse)
