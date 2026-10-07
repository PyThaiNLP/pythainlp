# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenize text into Thai Character Clusters (TCCs).

The implementation follows the TCC rules proposed by Theeramunkong et al.
2000:
https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2548

Credits:

* TCC: Jakkrit TeCho
* Grammar: Wittawat Jitkrittum
  (https://github.com/wittawatj/jtcc/blob/master/TCC.g)
* Python code: Korakot Chaovavanich
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

_RE_TCC: list[str] = (
    """\
c[ั]([่-๋]c)?
c[ั]([่-๋]c)?k
เc็ck
เcctาะk
เccีtยะk
เccีtย(?=[เ-ไก-ฮ]|$)k
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)k
เcc็ck
เcิc์ck
เcิtck
เcีtยะ?k
เcืtอะk
เcื
เctา?ะ?k
c[ึื]tck
c[ะ-ู]tk
c[ิุู]์
cรรc์
c็
ct[ะาำ]?k
แc็ck
แcc์k
แctะk
แcc็ck
แccc์k
โctะk
[เ-ไ]ctk
ก็
อึ
หึ
""".replace("k", "(cc?[d|ิ]?[์])?")
    .replace("c", "[ก-ฮ]")
    .replace("t", "[่-๋]?")
    .replace("d", "อูอุ".replace("อ", ""))  # DSara: lower vowel
    .split()
)

_PAT_TCC: re.Pattern[str] = re.compile("|".join(_RE_TCC))


def tcc(text: str) -> Iterator[str]:
    """
    Generate Thai Character Clusters (TCCs) from text.

    :param str text: text to be tokenized
    :return: iterator of character clusters
    :rtype: collections.abc.Iterator[str]
    """
    if not text or not isinstance(text, str):
        return

    len_text = len(text)
    p = 0
    while p < len_text:
        m = _PAT_TCC.match(text[p:])
        if m:
            n = m.span()[1]
        else:
            n = 1
        yield text[p : p + n]
        p += n


def tcc_pos(text: str) -> set[int]:
    """
    Get the ending positions of Thai Character Clusters (TCCs) in text.

    :param str text: text to be tokenized
    :return: set of ending positions of character clusters
    :rtype: set[int]
    """
    if not text or not isinstance(text, str):
        return set()

    p_set = set()
    p = 0
    for w in tcc(text):
        p += len(w)
        p_set.add(p)

    return p_set


def segment(text: str) -> list[str]:
    """
    Tokenize text into Thai Character Clusters (TCCs).

    :param str text: text to be tokenized
    :return: list of character clusters
    :rtype: list[str]
    """
    return list(tcc(text))
