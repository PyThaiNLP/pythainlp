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
    :param list data: a list of strings to be sorted
    :param bool reverse: reverse flag, set to get the result in descending order
    :return: a list of strings, sorted alphabetically, according to Thai rules
    **Example**::
        >>> from pythainlp.util import *
        >>> collate(['ไก่', 'เป็ด', 'หมู', 'วัว'])
        ['ไก่', 'เป็ด', 'วัว', 'หมู']
    """
    return sorted(data, key=_thkey, reverse=reverse)
