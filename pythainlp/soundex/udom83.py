# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai soundex - Udom83 system

Original paper:
Wannee Udompanich. String searching for Thai alphabet
using Soundex compression technique. Master Thesis
of Department of Computer Engineering Graduate
School, Chulalongkorn University, 1983.
https://cuir.car.chula.ac.th/handle/123456789/48471

Python implementation:
by Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""

from __future__ import annotations

import re
from typing import Pattern

from pythainlp import thai_consonants

_THANTHAKHAT: str = "\u0e4c"
_RE_1: Pattern[str] = re.compile(r"รร([\u0e40-\u0e44])")  # เ-ไ
_RE_2: Pattern[str] = re.compile(
    f"รร([{thai_consonants}][{thai_consonants}\u0e40-\u0e44])"
)
_RE_3: Pattern[str] = re.compile(
    f"รร([{thai_consonants}][\u0e30-\u0e39\u0e48-\u0e4c])"
)
_RE_4: Pattern[str] = re.compile(r"รร")
_RE_5: Pattern[str] = re.compile(f"ไ([{thai_consonants}]ย)")
_RE_6: Pattern[str] = re.compile(f"[ไใ]([{thai_consonants}])")
_RE_7: Pattern[str] = re.compile(r"\u0e33(ม[\u0e30-\u0e39])")
_RE_8: Pattern[str] = re.compile(r"\u0e33ม")
_RE_9: Pattern[str] = re.compile(r"\u0e33")  # ำ
_RE_10: Pattern[str] = re.compile(
    f"จน์|มณ์|ณฑ์|ทร์|ตร์|"
    f"[{thai_consonants}]{_THANTHAKHAT}|[{thai_consonants}]"
    f"[\u0e30-\u0e39]{_THANTHAKHAT}"
)
_RE_11: Pattern[str] = re.compile(r"[\u0e30-\u0e4c]")

_TRANS1: dict[int, int] = str.maketrans(
    "กขฃคฅฆงจฉชฌซศษสฎดฏตฐฑฒถทธณนบปผพภฝฟมญยรลฬฤฦวอหฮ",
    "กขขขขขงจชชชสสสสดดตตททททททนนบปพพพฟฟมยยรรรรรวอฮฮ",
)
_TRANS2: dict[int, int] = str.maketrans(
    "มวำกขฃคฅฆงยญณนฎฏดตศษสบปพภผฝฟหอฮจฉชซฌฐฑฒถทธรฤลฦ",
    "0001111112233344444445555666666777778888889999",
)


def udom83(text: str) -> str:
    """Converts Thai text into phonetic code with the
    Thai soundex algorithm named **Udom83** [#udom83]_.

    :param str text: Thai word

    :return: Udom83 soundex
    :rtype: str

    :Example:

        >>> from pythainlp.soundex import udom83
        >>> udom83("ลัก")
        'ร100000'
        >>> udom83("รัก")
        'ร100000'
        >>> udom83("รักษ์")
        'ร100000'
        >>> udom83("บูรณการ")
        'บ931900'
        >>> udom83("ปัจจุบัน")
        'ป775300'
    """
    if not text or not isinstance(text, str):
        return ""

    text = _RE_1.sub("ัน\\1", text)
    text = _RE_2.sub("ั\\1", text)
    text = _RE_3.sub("ัน\\1", text)
    text = _RE_4.sub("ัน", text)
    text = _RE_5.sub("\\1", text)
    text = _RE_6.sub("\\1ย", text)
    text = _RE_7.sub("ม\\1", text)
    text = _RE_8.sub("ม", text)
    text = _RE_9.sub("ม", text)
    text = _RE_10.sub("", text)
    text = _RE_11.sub("", text)

    if not text:
        return ""

    sd = "".join(
        [text[0].translate(_TRANS1), text[1:].translate(_TRANS2), "000000"]
    )

    return sd[:7]
