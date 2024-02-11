# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex - Udom83 system

Original paper:
Wannee Udompanich. String searching for Thai alphabet
using Soundex compression technique. Master Thesis
of Department of Computer Engineering Graduate
School, Chulalongkorn University, 1983.
http://cuir.car.chula.ac.th/handle/123456789/48471

Python implementation:
by Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""
import re

from pythainlp import thai_consonants

_THANTHAKHAT = "\u0e4c"
_RE_1 = re.compile(r"รร([\u0e40-\u0e44])")  # เ-ไ
_RE_2 = re.compile(f"รร([{thai_consonants}][{thai_consonants}\u0e40-\u0e44])")
_RE_3 = re.compile(f"รร([{thai_consonants}][\u0e30-\u0e39\u0e48-\u0e4c])")
_RE_4 = re.compile(r"รร")
_RE_5 = re.compile(f"ไ([{thai_consonants}]ย)")
_RE_6 = re.compile(f"[ไใ]([{thai_consonants}])")
_RE_7 = re.compile(r"\u0e33(ม[\u0e30-\u0e39])")
_RE_8 = re.compile(r"\u0e33ม")
_RE_9 = re.compile(r"\u0e33")  # ำ
_RE_10 = re.compile(
    f"จน์|มณ์|ณฑ์|ทร์|ตร์|"
    f"[{thai_consonants}]{_THANTHAKHAT}|[{thai_consonants}]"
    f"[\u0e30-\u0e39]{_THANTHAKHAT}"
)
_RE_11 = re.compile(r"[\u0e30-\u0e4c]")

_TRANS1 = str.maketrans(
    "กขฃคฅฆงจฉชฌซศษสฎดฏตฐฑฒถทธณนบปผพภฝฟมญยรลฬฤฦวอหฮ",
    "กขขขขขงจชชชสสสสดดตตททททททนนบปพพพฟฟมยยรรรรรวอฮฮ",
)
_TRANS2 = str.maketrans(
    "มวำกขฃคฅฆงยญณนฎฏดตศษสบปพภผฝฟหอฮจฉชซฌฐฑฒถทธรฤลฦ",
    "0001111112233344444445555666666777778888889999",
)


def udom83(text: str) -> str:
    """
    This function converts Thai text into phonetic code with the
    Thai soundex algorithm named **Udom83** [#udom83]_.

    :param str text: Thai word

    :return: Udom83 soundex
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex import udom83

        udom83("ลัก")
        # output : 'ล100'

        udom83("รัก")
        # output: 'ร100'

        udom83("รักษ์")
        # output: 'ร100'

        udom83("บูรณการ")
        # output: 'บ5515'

        udom83("ปัจจุบัน")
        # output: 'ป775300'
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
