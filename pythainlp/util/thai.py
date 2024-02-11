# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Check if it is Thai text
"""
import string
from typing import Tuple

from pythainlp import (
    thai_lead_vowels,
    thai_follow_vowels,
    thai_above_vowels,
    thai_below_vowels,
    thai_consonants,
    thai_vowels,
    thai_tonemarks,
    thai_signs,
    thai_digits,
    thai_punctuations,
)
from pythainlp.transliterate import pronunciate
from pythainlp.util.syllable import tone_detector

_DEFAULT_IGNORE_CHARS = string.whitespace + string.digits + string.punctuation
_TH_FIRST_CHAR_ASCII = 3584
_TH_LAST_CHAR_ASCII = 3711


def isthaichar(ch: str) -> bool:
    """Check if a character is a Thai character.

    :param ch: input character
    :type ch: str
    :return: True if ch is a Thai character, otherwise False.
    :rtype: bool

    :Example:
    ::

        from pythainlp.util import isthaichar

        isthaichar("ก")  # THAI CHARACTER KO KAI
        # output: True

        isthaichar("๕")  # THAI DIGIT FIVE
        # output: True
    """
    ch_val = ord(ch)
    if _TH_FIRST_CHAR_ASCII <= ch_val <= _TH_LAST_CHAR_ASCII:
        return True
    return False


def isthai(text: str, ignore_chars: str = ".") -> bool:
    """Check if every character in a string is a Thai character.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to "."
    :type ignore_chars: str, optional
    :return: True if every character in the input string is Thai,
             otherwise False.
    :rtype: bool

    :Example:
    ::

        from pythainlp.util import isthai

        isthai("กาลเวลา")
        # output: True

        isthai("กาลเวลา.")
        # output: True

        isthai("กาล-เวลา")
        # output: False

        isthai("กาล-เวลา +66", ignore_chars="01234567890+-.,")
        # output: True

    """
    if not ignore_chars:
        ignore_chars = ""

    for ch in text:
        if ch not in ignore_chars and not isthaichar(ch):
            return False
    return True


def countthai(text: str, ignore_chars: str = _DEFAULT_IGNORE_CHARS) -> float:
    """Find proportion of Thai characters in a given text

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to whitespace,\\
        digits, and punctuation marks.
    :type ignore_chars: str, optional
    :return: proportion of Thai characters in the text (percentage)
    :rtype: float

    :Example:
    ::

        from pythainlp.util import countthai

        countthai("ไทยเอ็นแอลพี 3.0")
        # output: 100.0

        countthai("PyThaiNLP 3.0")
        # output: 0.0

        countthai("ใช้งาน PyThaiNLP 3.0")
        # output: 40.0

        countthai("ใช้งาน PyThaiNLP 3.0", ignore_chars="")
        # output: 30.0
    """
    if not text or not isinstance(text, str):
        return 0.0

    if not ignore_chars:
        ignore_chars = ""

    num_thai = 0
    num_ignore = 0

    for ch in text:
        if ch in ignore_chars:
            num_ignore += 1
        elif isthaichar(ch):
            num_thai += 1

    num_count = len(text) - num_ignore

    if num_count == 0:
        return 0.0

    return (num_thai / num_count) * 100


def display_thai_char(ch: str) -> str:
    """Prefix an underscore (_) to a high-position vowel or a tone mark,
    to ease readability.

    :param ch: input character
    :type ch: str
    :return: "_" + ch
    :rtype: str

    :Example:
    ::

        from pythainlp.util import display_thai_char

        display_thai_char("้")
        # output: "_้"
    """

    if (
        ch in thai_above_vowels
        or ch in thai_tonemarks
        or ch in "\u0e33\u0e4c\u0e4d\u0e4e"
    ):
        # last condition is Sra Aum, Thanthakhat, Nikhahit, Yamakkan
        return "_" + ch
    else:
        return ch


def thai_word_tone_detector(word: str) -> Tuple[str, str]:
    """
    Thai tone detector for word.

    It uses pythainlp.transliterate.pronunciate for converting word to\
        pronunciation.

    :param str word: Thai word.
    :return: Thai pronunciation with tones in each syllable.\
        (l, m, h, r, f or empty if it cannot be detected)
    :rtype: Tuple[str, str]

    :Example:
    ::

        from pythainlp.util import thai_word_tone_detector

        print(thai_word_tone_detector("คนดี"))
        # output: [('คน', 'm'), ('ดี', 'm')]

        print(thai_word_tone_detector("มือถือ"))
        # output: [('มือ', 'm'), ('ถือ', 'r')]
    """
    _pronunciate = pronunciate(word).split("-")
    return [(i, tone_detector(i.replace("หฺ", "ห"))) for i in _pronunciate]


def count_thai_chars(text: str) -> dict:
    """
    Count Thai characters by type

    This function will give you numbers of Thai characters by type\
        (consonants, vowels, lead_vowels, follow_vowels, above_vowels,\
        below_vowels, tonemarks, signs, thai_digits, punctuations, non_thai)

    :param str text: Text
    :return: Dict with numbers of Thai characters by type
    :rtype: dict

    :Example:
    ::

        from pythainlp.util import count_thai_chars

        count_thai_chars("ทดสอบภาษาไทย")
        # output: {
        # 'vowels': 3,
        # 'lead_vowels': 1,
        # 'follow_vowels': 2,
        # 'above_vowels': 0,
        # 'below_vowels': 0,
        # 'consonants': 9,
        # 'tonemarks': 0,
        # 'signs': 0,
        # 'thai_digits': 0,
        # 'punctuations': 0,
        # 'non_thai': 0
        # }
    """
    _dict = {
        "vowels": 0,
        "lead_vowels": 0,
        "follow_vowels": 0,
        "above_vowels": 0,
        "below_vowels": 0,
        "consonants": 0,
        "tonemarks": 0,
        "signs": 0,
        "thai_digits": 0,
        "punctuations": 0,
        "non_thai": 0,
    }
    for c in text:
        if c in thai_vowels:
            _dict["vowels"] += 1
        if c in thai_lead_vowels:
            _dict["lead_vowels"] += 1
        elif c in thai_follow_vowels:
            _dict["follow_vowels"] += 1
        elif c in thai_above_vowels:
            _dict["above_vowels"] += 1
        elif c in thai_below_vowels:
            _dict["below_vowels"] += 1
        elif c in thai_consonants:
            _dict["consonants"] += 1
        elif c in thai_tonemarks:
            _dict["tonemarks"] += 1
        elif c in thai_signs:
            _dict["signs"] += 1
        elif c in thai_digits:
            _dict["thai_digits"] += 1
        elif c in thai_punctuations:
            _dict["punctuations"] += 1
        else:
            _dict["non_thai"] += 1
    return _dict
