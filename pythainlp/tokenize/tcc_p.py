# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenize text into Thai Character Clusters (TCCs) with improved rules.

The implementation follows the TCC rules proposed by Theeramunkong et al.
2000 (https://doi.org/10.1145/355214.355225),
and the improved rules that newmm uses.

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
เc็ck
เcctาะk
เccีtยะk
เccีtย(?=[เ-ไก-ฮ]|$)k
เcc็ck
เcิc์ck
เcิtck
เcีtยะ?k
เcืtอะ?k
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)k
เctา?ะ?k
cัtวะk
c[ัื]tc[ุิะ]?k
c[ิุู]์
c[ะ-ู]tk
cรรc์
c็
ct[ะาำ]?k
ck
แc็c
แcc์
แctะ
แcc็c
แccc์
โctะ
[เ-ไ]ct
ก็
อึ
หึ
""".replace("k", "(cc?[dิ]?[์])?")
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
        m = _PAT_TCC.match(text, p)
        n = m.end() - p if m else 1
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


def tcc_pos_array(text: str) -> bytearray:
    """
    Get the valid Thai Character Cluster (TCC) boundaries as a bytearray.

    The bytearray has length ``len(text) + 1``. Index ``i`` is ``1`` if
    position ``i`` is a valid TCC boundary, and ``0`` otherwise.
    Array-index lookup is faster and uses less memory than set membership
    for large text.

    :param str text: text to be tokenized
    :return: bytearray of valid TCC boundary flags, indexed by position
    :rtype: bytearray
    """
    if not text or not isinstance(text, str):
        return bytearray(1)

    arr = bytearray(len(text) + 1)
    p = 0
    for w in tcc(text):
        p += len(w)
        arr[p] = 1

    return arr


def segment(text: str) -> list[str]:
    """
    Tokenize text into Thai Character Clusters (TCCs).

    :param str text: text to be tokenized
    :return: list of character clusters
    :rtype: list[str]
    """
    return list(tcc(text))
