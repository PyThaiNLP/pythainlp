# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex - LK82 system

Original paper:
Vichit Lorchirachoonkul. 1982. A Thai soundex
system. Information Processing & Management,
18(5):243–255.
https://doi.org/10.1016/0306-4573(82)90003-6

Python implementation:
by Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""
import re

from pythainlp.util import remove_tonemark

_TRANS1 = str.maketrans(
    "กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ",
    "กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ",
)
_TRANS2 = str.maketrans(
    "กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ",
    "1111112333333333333333333444444445555555667777889AAABCDEEF",
)

# silenced
_RE_KARANT = re.compile(r"จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์")

# signs, symbols, vowel that has no explicit sounds
# Paiyannoi, Phinthu, Maiyamok, Maitaikhu, Nikhahit
_RE_SIGN = re.compile(r"[\u0e2f\u0e3a\u0e46\u0e47\u0e4d]")


def lk82(text: str) -> str:
    """
    This function converts Thai text into phonetic code with the
    Thai soundex algorithm named **LK82** [#lk82]_.

    :param str text: Thai word

    :return: LK82 soundex of the given Thai word
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex import lk82

        lk82("ลัก")
        # output: 'ร1000'

        lk82("รัก")
        # output: 'ร1000'

        lk82("รักษ์")
        # output: 'ร1000'

        lk82("บูรณการ")
        # output: 'บE419'

        lk82("ปัจจุบัน")
        # output: 'ป3E54'
    """
    if not text or not isinstance(text, str):
        return ""

    text = remove_tonemark(text)  # 4. remove tone marks
    text = _RE_KARANT.sub("", text)  # 4. remove "karat" characters
    text = _RE_SIGN.sub("", text)  # 5. remove Mai tai khu,

    if not text:
        return ""

    # 6. encode the first character
    res = []
    if "ก" <= text[0] <= "ฮ":
        res.append(text[0].translate(_TRANS1))
        text = text[1:]
    else:
        if len(text) > 1:
            res.append(text[1].translate(_TRANS1))
        res.append(text[0].translate(_TRANS2))
        text = text[2:]

    # encode the rest
    i_v = None  # ตำแหน่งตัวคั่นล่าสุด (สระ)
    len_text = len(text)
    for i, c in enumerate(text):
        if (
            c in "\u0e30\u0e31\u0e34\u0e35"
        ):  # 7. ตัวคั่นเฉยๆ/ Sara A, Mai Han-Akat, Sara I, Sara II
            i_v = i
            res.append("")
        elif (
            c in "\u0e32\u0e36\u0e37\u0e39\u0e45"
        ):  # 8. คั่นและใส่/ Sara Aa, Sara Ue, Sara Uee, Sara Uu, Lankkhangyao
            i_v = i
            res.append(c.translate(_TRANS2))
        elif c == "\u0e38":  # 9. สระอุ / Sara U
            i_v = i
            if i == 0 or (text[i - 1] not in "ตธ"):
                res.append(c.translate(_TRANS2))
            else:
                res.append("")
        elif c in "\u0e2b\u0e2d":  # หอ
            if i + 1 < len_text and (
                text[i + 1] in "\u0e36\u0e37\u0e38\u0e39"
            ):  # Sara Ue, Sara Uee, Sara U, Sara Uu
                res.append(c.translate(_TRANS2))
        elif c in "\u0e22\u0e23\u0e24\u0e26\u0e27":
            if i_v == i - 1 or (
                i + 1 < len_text
                and (text[i + 1] in "\u0e36\u0e37\u0e38\u0e39")
            ):  # Sara Ue, Sara Uee, Sara U, Sara Uu
                res.append(c.translate(_TRANS2))
        else:
            res.append(c.translate(_TRANS2))  # 12.

    # 13. remove repetitions
    res2 = [res[0]]
    for i in range(1, len(res)):
        if res[i] != res[i - 1]:
            res2.append(res[i])

    # 14. fill with zeros
    return ("".join(res2) + "0000")[:5]
