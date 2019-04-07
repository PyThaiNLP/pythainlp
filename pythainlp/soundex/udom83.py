# -*- coding: utf-8 -*-
"""
Thai soundex - Udom83 system

Python implementation: Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""
import re

_RE_1 = re.compile(r"รร([เ-ไ])")
_RE_2 = re.compile(r"รร([ก-ฮ][ก-ฮเ-ไ])")
_RE_3 = re.compile(r"รร([ก-ฮ][ะ-ู่-์])")
_RE_4 = re.compile(r"รร")
_RE_5 = re.compile(r"ไ([ก-ฮ]ย)")
_RE_6 = re.compile(r"[ไใ]([ก-ฮ])")
_RE_7 = re.compile(r"ำ(ม[ะ-ู])")
_RE_8 = re.compile(r"ำม")
_RE_9 = re.compile(r"ำ")
_RE_10 = re.compile(r"จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์")
_RE_11 = re.compile(r"[ะ-์]")

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
    Udom83 - It's a Thai soundex rule.

    :param str text: Thai word
    :return: Udom83 soundex
    """

    if not text:
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

    sd = text[0].translate(_TRANS1)
    sd += text[1:].translate(_TRANS2)

    return (sd + "000000")[:7]
