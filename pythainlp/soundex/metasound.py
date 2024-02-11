# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex - MetaSound system

References:
Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with
a Statistical Ontology for Analysing Names Given in Accordance
with Thai Astrology.
https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
"""

_CONS_THANTHAKHAT = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ์"
_THANTHAKHAT = "์"  # \u0e4c
_C1 = "กขฃคฆฅ"  # sound K -> coded letter 1
_C2 = "จฉชฌซฐทฒดฎตสศษ"  # D -> 2
_C3 = "ฟฝพผภบป"  # B -> 3
_C4 = "ง"  # NG -> 4
_C5 = "ลฬรนณฦญ"  # N -> 5
_C6 = "ม"  # M -> 6
_C7 = "ย"  # Y -> 7
_C8 = "ว"  # W -> 8


def metasound(text: str, length: int = 4) -> str:
    """
    This function converts Thai text into phonetic code with the
    matching technique called **MetaSound**
    [#metasound]_ (combination between Soundex and Metaphone algorithms).
    MetaSound algorithm was developed specifically for the Thai language.

    :param str text: Thai text
    :param int length: preferred length of the MetaSound code (default is 4)

    :return: MetaSound for the given text
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex.metasound import metasound

        metasound("ลัก")
        # output: 'ล100'

        metasound("รัก")
        # output: 'ร100'

        metasound("รักษ์")
        # output: 'ร100'

        metasound("บูรณการ", 5)
        # output: 'บ5515'

        metasound("บูรณการ", 6))
        # output: 'บ55150'

        metasound("บูรณการ", 4)
        # output: 'บ551'
    """
    if not text or not isinstance(text, str):
        return ""

    # keep only consonants and thanthakhat
    chars = []
    for ch in text:
        if ch in _CONS_THANTHAKHAT:
            chars.append(ch)

    # remove karan (thanthakhat and a consonant before it)
    i = 0
    while i < len(chars):
        if chars[i] == _THANTHAKHAT:
            if i > 0:
                chars[i - 1] = " "
            chars[i] = " "
        i += 1

    # retain first consonant, encode the rest
    chars = chars[:length]
    i = 1
    while i < len(chars):
        if chars[i] in _C1:
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
        elif chars[i] in _C7:
            chars[i] = "7"
        elif chars[i] in _C8:
            chars[i] = "8"
        else:
            chars[i] = "0"
        i += 1

    while len(chars) < length:
        chars.append("0")

    return "".join(chars)
