# -*- coding: utf-8 -*-
"""
Thai collation (sort according to Thai dictionary order)
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
    This function sorts a list of strings according to Thai alphabets.

    :param list[str] data: a list of words to be sorted
    :param bool reverse: If `reverse` is set to **True** the result will be
                         sorted in descending order. Otherwise, the result will
                         be sorted in ascending order.
                         By default, the parameter `reverse` is set to
                         **False**, sorting alphabettically in ascending order.

    :return: a list of strings, sorted alphabetically, according to
             Thai alphabets
    :rtype: list[str]

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
