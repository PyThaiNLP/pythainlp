# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai collation (sorted according to Thai dictionary order)
Simple implementation using regular expressions
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Pattern

if TYPE_CHECKING:
    from collections.abc import Iterable

_RE_TONE: Pattern[str] = re.compile(r"[็-์]")
_RE_LV_C: Pattern[str] = re.compile(r"([เ-ไ])([ก-ฮ])")


def _thkey(word: str) -> str:
    cv = _RE_TONE.sub("", word)  # remove tone
    cv = _RE_LV_C.sub("\\2\\1", cv)  # switch lead vowel

    tone_match = _RE_TONE.search(word)
    tone = tone_match.group() if tone_match else ""
    return cv + tone


def collate(data: Iterable[str], reverse: bool = False) -> list[str]:
    """Sorts strings (almost) according to Thai dictionary.

    Important notes: this implementation ignores tone marks and symbols

    :param data: an iterable of words to be sorted
    :type data: Iterable[str]
    :param reverse: If `reverse` is set to **True** the result will be
                         sorted in descending order. Otherwise, the result
                         will be sorted in ascending order, defaults to False
    :type reverse: bool, optional

    :return: a list of strings, sorted alphabetically, (almost) according to
             Thai dictionary
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util import collate
        >>> collate(['ไก่', 'เกิด', 'กาล', 'เป็ด', 'หมู', 'วัว', 'วันที่'])
        ['กาล', 'เกิด', 'ไก่', 'เป็ด', 'วันที่', 'วัว', 'หมู']
        >>> collate(['ไก่', 'เกิด', 'กาล', 'เป็ด', 'หมู', 'วัว', 'วันที่'],
        ...     reverse=True)
        ['หมู', 'วัว', 'วันที่', 'เป็ด', 'ไก่', 'เกิด', 'กาล']
    """
    return sorted(data, key=_thkey, reverse=reverse)
