# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai-English Cross-Language Transliterated Word Retrieval
using Soundex Technique

References:
Prayut Suwanvisat, Somchai Prasitjutrakul.Thai-English Cross-Language Transliterated Word Retrieval using Soundex Technique. In 1998 [cited 2022 Sep 8]. Available from: https://www.cp.eng.chula.ac.th/~somchai/spj/papers/ThaiText/ncsec98-clir.pdf
"""
from pythainlp import thai_characters

_C0 = "AEIOUHWYอ"
_C1 = "BFPVบฝฟปผพภว"
_C2 = "CGJKQSXZขฃคฅฆฉขฌกจซศษส"
_C3 = "DTฎดฏตฐฑฒถทธ"
_C4 = "Lลฬ"
_C5 = "MNมณน"
_C6 = "Rร"
_C7 = "AEIOUอ"
_C8 = "Hหฮ"
_C1_1 = "Wว"
_C9 = "Yยญ"
_C52 = "ง"


def prayut_and_somchaip(text: str, length: int = 4) -> str:
    """
    This function converts English-Thai Cross-Language Transliterated Word into
    phonetic code with the matching technique called **Soundex** [#prayut_and_somchaip]_.

    :param str text: English-Thai Cross-Language Transliterated Word
    :param int length: preferred length of the Soundex code (default is 4)

    :return: Soundex for the given text
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip

        prayut_and_somchaip("king", 2)
        # output: '52'

        prayut_and_somchaip("คิง", 2)
        # output: '52'
    """
    if not text or not isinstance(text, str):
        return ""
    text = text.upper()
    # keep only consonants (English-Thai)
    chars = []
    for ch in text:
        if ch in thai_characters + "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            chars.append(ch)

    i = 0
    while i < len(chars):
        if i == 0 and chars[i] in _C0:
            chars[i] = "0"
        elif chars[i] in _C1:
            chars[i] = "1"
        elif chars[i] in _C2:
            chars[i] = "2"
        elif chars[i] in _C3:
            chars[i] = "3"
        elif chars[i] in _C4:
            chars[i] = "4"
        elif chars[i] in _C5:
            chars[i] = "5"
        elif chars[i] in _C6:
            chars[i] = "6"
        elif chars[i] in _C52:
            chars[i] = "52"
        elif chars[i] in _C7 and i != 0:
            chars[i] = "7"
        elif chars[i] in _C8 and i != 0:
            chars[i] = "8"
        elif chars[i] in _C1_1 and i != 0:
            chars[i] = "1"
        elif chars[i] in _C9 and i != 0:
            chars[i] = "9"
        else:
            chars[i] = None
        i += 1
    chars = list("".join([i for i in chars if i is not None]))
    return "".join(chars[-length:])
