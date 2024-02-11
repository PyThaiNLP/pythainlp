# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
The Royal Thai General System of Transcription (RTGS)
is the official system for rendering Thai words in the Latin alphabet.
It was published by the Royal Institute of Thailand.

:See Also:
    * `Wikipedia <https://en.wikipedia.org/wiki/Royal_Thai_General_System_of_Transcription>`_
"""
import re

from pythainlp import thai_consonants, word_tokenize

# vowel
_vowel_patterns = """เ*ียว,\\1iao
แ*็ว,\\1aeo
เ*ือย,\\1ueai
แ*ว,\\1aeo
เ*็ว,\\1eo
เ*ว,\\1eo
*ิว,\\1io
*วย,\\1uai
เ*ย,\\1oei
*อย,\\1oi
โ*ย,\\1oi
*ุย,\\1ui
*าย,\\1ai
ไ*ย,\\1ai
*ัย,\\1ai
ไ**,\\1\\2ai
ไ*,\\1ai
ใ*,\\1ai
*ว*,\\1ua\\2
*ัวะ,\\1ua
*ัว,\\1ua
เ*ือะ,\\1uea
เ*ือ,\\1uea
เ*ียะ,\\1ia
เ*ีย,\\1ia
เ*อะ,\\1oe
เ*อ,\\1oe
เ*ิ,\\1oe
*อ,\\1o
เ*าะ,\\1o
เ*็,\\1e
โ*ะ,\\1o
โ*,\\1o
แ*ะ,\\1ae
แ*,\\1ae
เ*าะ,\\1e
*าว,\\1ao
เ*า,\\1ao
เ*,\\1e
*ู,\\1u
*ุ,\\1u
*ื,\\1ue
*ึ,\\1ue
*ี,\\1i
*ิ,\\1i
*ำ,\\1am
*า,\\1a
*ั,\\1a
*ะ,\\1a
#ฤ,\\1rue
$ฤ,\\1ri"""
_vowel_patterns = _vowel_patterns.replace("*", f"([{thai_consonants}])")
_vowel_patterns = _vowel_patterns.replace("#", "([คนพมห])")
_vowel_patterns = _vowel_patterns.replace("$", "([กตทปศส])")

_VOWELS = [x.split(",") for x in _vowel_patterns.split("\n")]

# พยัญชนะ ต้น สะกด
_CONSONANTS = {
    "ก": ["k", "k"],
    "ข": ["kh", "k"],
    "ฃ": ["kh", "k"],
    "ค": ["kh", "k"],
    "ฅ": ["kh", "k"],
    "ฆ": ["kh", "k"],
    "ง": ["ng", "ng"],
    "จ": ["ch", "t"],
    "ฉ": ["ch", "t"],
    "ช": ["ch", "t"],
    "ซ": ["s", "t"],
    "ฌ": ["ch", "t"],
    "ญ": ["y", "n"],
    "ฎ": ["d", "t"],
    "ฏ": ["t", "t"],
    "ฐ": ["th", "t"],
    # ฑ พยัญชนะต้น เป็น d ได้
    "ฑ": ["th", "t"],
    "ฒ": ["th", "t"],
    "ณ": ["n", "n"],
    "ด": ["d", "t"],
    "ต": ["t", "t"],
    "ถ": ["th", "t"],
    "ท": ["th", "t"],
    "ธ": ["th", "t"],
    "น": ["n", "n"],
    "บ": ["b", "p"],
    "ป": ["p", "p"],
    "ผ": ["ph", "p"],
    "ฝ": ["f", "p"],
    "พ": ["ph", "p"],
    "ฟ": ["f", "p"],
    "ภ": ["ph", "p"],
    "ม": ["m", "m"],
    "ย": ["y", ""],
    "ร": ["r", "n"],
    "ฤ": ["rue", ""],
    "ล": ["l", "n"],
    "ว": ["w", ""],
    "ศ": ["s", "t"],
    "ษ": ["s", "t"],
    "ส": ["s", "t"],
    "ห": ["h", ""],
    "ฬ": ["l", "n"],
    "อ": ["", ""],
    "ฮ": ["h", ""],
}

_THANTHAKHAT = "\u0e4c"
_RE_CONSONANT = re.compile(f"[{thai_consonants}]")
_RE_NORMALIZE = re.compile(
    f"จน์|มณ์|ณฑ์|ทร์|ตร์|[{thai_consonants}]{_THANTHAKHAT}|"
    f"[{thai_consonants}][\u0e30-\u0e39]{_THANTHAKHAT}"
    # Paiyannoi, Maiyamok, Tonemarks, Thanthakhat, Nikhahit, other signs
    r"|[\u0e2f\u0e46\u0e48-\u0e4f\u0e5a\u0e5b]"
)


def _normalize(word: str) -> str:
    """
    Remove silence, no sound, and tonal characters.

    ตัดอักษรที่ไม่ออกเสียง (การันต์ ไปยาลน้อย ไม้ยมก*) และวรรณยุกต์ทิ้ง
    """
    return _RE_NORMALIZE.sub("", word)


def _replace_vowels(word: str) -> str:
    for vowel in _VOWELS:
        word = re.sub(vowel[0], vowel[1], word)

    return word


def _replace_consonants(word: str, consonants: str) -> str:
    _HO_HIP = "\u0e2b"  # ห
    _RO_RUA = "\u0e23"  # ร
    _DOUBLE_RO_RUA = _RO_RUA + _RO_RUA

    if not consonants:
        return word

    skip = False
    mod_chars = []
    j = 0  # j is the index of consonants
    for i in range(len(word)):
        if skip:
            skip = False
            j += 1
        elif word[i] not in _CONSONANTS:  # word[i] is not a Thai consonant.
            mod_chars.append(word[i])
        elif (
            len(mod_chars) == 0 and word[i] == _HO_HIP and len(consonants) != 1
        ):  # Skip HO HIP except that HO HIP is the only one consonant
            j += 1
        elif (
            len(mod_chars) == 0
        ):  # The first character must be an initial consonant.
            mod_chars.append(_CONSONANTS[consonants[j]][0])
            j += 1
        elif word[i:] == _DOUBLE_RO_RUA:  # Double RO RUA is in end of word
            skip = True
            mod_chars.append("a")
            mod_chars.append("n")
            j += 1
        elif word[i : i + 2] == _DOUBLE_RO_RUA:
            skip = True
            mod_chars.append("a")
            j += 1
        else:  # Assume that the rest are final consonants.
            mod_chars.append(_CONSONANTS[consonants[j]][1])
            j += 1
    return "".join(mod_chars)


# support function for romanize()
def _romanize(word: str) -> str:
    word = _replace_vowels(_normalize(word))
    consonants = _RE_CONSONANT.findall(word)

    # 2-character word, all consonants
    if len(word) == 2 and len(consonants) == 2:
        word = list(word)
        word.insert(1, "o")
        word = "".join(word)

    word = _replace_consonants(word, consonants)
    return word


def romanize(text: str) -> str:
    """Render Thai words in Latin alphabet, using RTGS

    Royal Thai General System of Transcription (RTGS),
    is the official system by the Royal Institute of Thailand.

    :param text: Thai text to be romanized
    :type text: str
    :return: A string of Thai words rendered in the Latin alphabet
    :rtype: str
    """
    words = word_tokenize(text)
    romanized_words = [_romanize(word) for word in words]

    return "".join(romanized_words)
