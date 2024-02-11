# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Transliterating Thai text using ISO 11940

:See Also:
    * `Wikipedia \
        <https://en.wikipedia.org/wiki/ISO_11940>`_
"""
_consonants = {
    "ก": "k",
    "ข": "k̄h",
    "ฃ": "ḳ̄h",
    "ค": "kh",
    "ฅ": "k̛h",
    "ฆ": "ḳh",
    "ง": "ng",
    "จ": "c",
    "ฉ": "c̄h",
    "ช": "ch",
    "ซ": "s",
    "ฌ": "c̣h",
    "ญ": "ỵ",
    "ฎ": "ḍ",
    "ฏ": "ṭ",
    "ฐ": "ṭ̄h",
    "ฑ": "ṯh",
    "ฒ": "t̛h",
    "ณ": "ṇ",
    "ด": "d",
    "ต": "t",
    "ถ": "t̄h",
    "ท": "th",
    "ธ": "ṭh",
    "น": "n",
    "บ": "b",
    "ป": "p",
    "ผ": "p̄h",
    "ฝ": "f̄",
    "พ": "ph",
    "ฟ": "f",
    "ภ": "p̣h",
    "ม": "m",
    "ย": "y",
    "ร": "r",
    "ฤ": "v",
    "ล": "l",
    "ฦ": "ł",
    "ว": "w",
    "ศ": "ṣ̄",
    "ษ": "s̛̄",
    "ส": "s̄",
    "ห": "h̄",
    "ฬ": "ḷ",
    "อ": "x",
    "ฮ": "ḥ",
}

_vowels = {
    "ะ": "a",
    "ั": "ạ",
    "า": "ā",
    "ำ": "å",
    "ิ": "i",
    "ี": "ī",
    "ึ": "ụ",
    "ื": "ụ̄",
    "ุ": "u",
    "ู": "ū",
    "เ": "e",
    "แ": "æ",
    "โ": "o",
    "ใ": "ı",
    "ไ": "ị",
    "ฤ": "v",
    "ฤๅ": "vɨ",
    "ฦ": "ł",
    "ฦๅ": "łɨ",
    "ย": "y",
    "ว": "w",
    "อ": "x",
}

_tone_marks = {
    "่": "–̀".replace("–", ""),
    "้": "–̂".replace("–", ""),
    "๊": "–́".replace("–", ""),
    "๋": "–̌".replace("–", ""),
    "็": "–̆".replace("–", ""),
    "์": "–̒".replace("–", ""),
    "–๎".replace("–", ""): "~",
    "–ํ".replace("–", ""): "–̊".replace("–", ""),
    "–ฺ".replace("–", ""): "–̥".replace("–", ""),
}

_punctuation_and_digits = {
    # ฯ can has two meanings in ISO 11940.
    # If it is for abbrevation, it is paiyan noi.
    # If it is for sentence termination, it is angkhan diao.
    # Without semantic analysis, they cannot be distinguished from each other.
    # In this simple implementation, we decided to always treat ฯ as paiyan noi.
    # We commented out angkhan diao line to remove it from the dictionary
    # and avoid having duplicate keys.
    "ๆ": "«",
    "ฯ": "ǂ",  # paiyan noi: U+01C2 ǂ Alveolar Click; ICU uses ‡ (double dagger)
    "๏": "§",
    # "ฯ": "ǀ",  # angkhan diao: U+01C0 ǀ Dental Click; ICU uses | (vertical bar)
    "๚": "ǁ",  # angkhan khu: U+01C1 ǁ Lateral Click; ICU uses || (two vertical bars)
    "๛": "»",
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
}

_all_dict = {
    **_consonants,
    **_vowels,
    **_tone_marks,
    **_punctuation_and_digits,
}
_keys_set = _all_dict.keys()


def transliterate(word: str) -> str:
    """
    Use ISO 11940 for transliteration
    :param str text: Thai text to be transliterated.
    :return: A string indicating how the text should be pronounced, according to ISO 11940.
    """
    _str = ""
    for i in word:
        if i in _keys_set:
            _str += _all_dict[i]
        else:
            _str += i
    return _str
