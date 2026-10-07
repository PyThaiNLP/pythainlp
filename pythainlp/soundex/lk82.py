# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex, LK82 system.

Original paper:
Vichit Lorchirachoonkul. 1982. A Thai soundex
system. Information Processing & Management,
18(5):243–255.
https://doi.org/10.1016/0306-4573(82)90003-6

Python implementation:
by Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""

from __future__ import annotations

import re
from re import Pattern
from typing import Optional

from pythainlp.util import remove_tonemark

_TRANS1: dict[int, int] = str.maketrans(
    "กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ",
    "กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ",
)
_TRANS2: dict[int, int] = str.maketrans(
    "กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ",
    "1111112333333333333333333444444445555555667777889AAABCDEEF",
)
_CODE2: dict[str, str] = {chr(k): chr(v) for k, v in _TRANS2.items()}

# silenced
_RE_KARANT: Pattern[str] = re.compile(r"จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์")

# signs, symbols, vowel that has no explicit sounds
# Paiyannoi, Phinthu, Maiyamok, Maitaikhu, Nikhahit
_RE_SIGN: Pattern[str] = re.compile(r"[\u0e2f\u0e3a\u0e46\u0e47\u0e4d]")


# Sara Ue, Sara Uee, Sara U, Sara Uu
_LONG_U: str = "\u0e36\u0e37\u0e38\u0e39"
# 7. separators without a code: Sara A, Mai Han-Akat, Sara I, Sara II
_SEPARATORS: str = "\u0e30\u0e31\u0e34\u0e35"
# 8. separators with a code: Sara Aa, Sara Ue, Sara Uee, Sara Uu, Lakkhangyao
_CODED_SEPARATORS: str = "\u0e32\u0e36\u0e37\u0e39\u0e45"
_SARA_U: str = "\u0e38"  # 9.
_ALL_SEPARATORS: str = _SEPARATORS + _CODED_SEPARATORS + _SARA_U
# separators 7. and 8. mapped to their codes
_SEPARATOR_CODE: dict[str, str] = {
    **dict.fromkeys(_SEPARATORS, ""),
    **{c: _CODE2[c] for c in _CODED_SEPARATORS},
}
_HO_O: str = "\u0e2b\u0e2d"  # Ho Hip, O Ang
_SEMIVOWELS: str = "\u0e22\u0e23\u0e24\u0e26\u0e27"
_SPECIAL: frozenset[str] = frozenset(_ALL_SEPARATORS + _HO_O + _SEMIVOWELS)


def _encode_first(text: str) -> tuple[list[str], str]:
    """6. Encode the first character; return the codes and the rest."""
    if "ก" <= text[0] <= "ฮ":
        return [text[0].translate(_TRANS1)], text[1:]
    codes = []
    if len(text) > 1:
        codes.append(text[1].translate(_TRANS1))
    codes.append(text[0].translate(_TRANS2))
    return codes, text[2:]


def _before_long_u(text: str, i: int) -> bool:
    """Check if text[i] is followed by a long U sara."""
    return i + 1 < len(text) and text[i + 1] in _LONG_U


def _encode_char(text: str, i: int, i_v: Optional[int]) -> Optional[str]:
    """
    Encode Sara U, Ho Hip, O Ang, or a semivowel at text[i].

    Return None when the character has no code, or "" for Sara U after
    ต/ธ (the empty string breaks repeat removal in step 13).
    The caller sets ``i_v`` for Sara U.

    :param str text: text after the first character
    :param int i: position of the character
    :param i_v: position of the latest separator (vowel)
    :type i_v: Optional[int]
    """
    c = text[i]
    if c == _SARA_U:
        if i == 0 or text[i - 1] not in "ตธ":
            return _CODE2.get(c, c)
        return ""
    if c in _HO_O:
        voiced = _before_long_u(text, i)
    else:
        voiced = i_v == i - 1 or _before_long_u(text, i)
    return _CODE2.get(c, c) if voiced else None


def _finish(res: list[str]) -> str:
    """13. Remove repetitions and 14. fill with zeros."""
    res2 = [res[0]]
    for code in res:
        if code != res2[-1]:
            res2.append(code)
    return ("".join(res2) + "0000")[:5]


def lk82(text: str) -> str:
    """
    Convert text into a LK82 phonetic code.

    LK82 [#lk82]_ is a Thai soundex algorithm.

    :param str text: Thai word to be encoded
    :return: LK82 soundex code
    :rtype: str

    :Example:

        >>> from pythainlp.soundex import lk82
        >>> lk82("ลัก")
        'ร1000'
        >>> lk82("รัก")
        'ร1000'
        >>> lk82("รักษ์")
        'ร1000'
        >>> lk82("บูรณการ")
        'บE419'
        >>> lk82("ปัจจุบัน")
        'ป3E54'
    """
    if not text or not isinstance(text, str):
        return ""

    text = remove_tonemark(text)  # 4. remove tone marks
    text = _RE_KARANT.sub("", text)  # 4. remove "karat" characters
    text = _RE_SIGN.sub("", text)  # 5. remove signs and symbols

    if not text:
        return ""

    res, text = _encode_first(text)

    i_v: Optional[int] = None  # position of the latest separator (vowel)
    for i, c in enumerate(text):
        if c not in _SPECIAL:  # 12. fast path for other characters
            res.append(_CODE2.get(c, c))
            continue
        code = _SEPARATOR_CODE.get(c)
        if code is None:
            if c == _SARA_U:  # 9.
                i_v = i
            code = _encode_char(text, i, i_v)
        else:
            i_v = i
        if code is not None:
            res.append(code)

    return _finish(res)
