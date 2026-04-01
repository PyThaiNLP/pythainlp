# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Check if it is Thai text"""

from __future__ import annotations

import string
from collections import defaultdict
from types import MappingProxyType
from typing import Optional

from pythainlp import (
    thai_above_vowels,
    thai_below_vowels,
    thai_consonants,
    thai_digits,
    thai_follow_vowels,
    thai_lead_vowels,
    thai_punctuations,
    thai_signs,
    thai_tonemarks,
    thai_vowels,
)
from pythainlp.tools import warn_deprecation

_DEFAULT_IGNORE_CHARS: str = (
    string.whitespace + string.digits + string.punctuation
)
_TH_FIRST_CHAR_ASCII: int = 3584
_TH_LAST_CHAR_ASCII: int = 3711

# A comprehensive map of Thai characters to their descriptive names.
# MappingProxyType makes this constant read-only at runtime.
_THAI_CHAR_NAMES: MappingProxyType[str, str] = MappingProxyType(
    {
        # Consonants
        **{char: char for char in thai_consonants},
        # Vowels and Signs
        "\u0e24": "ฤ",
        "\u0e26": "ฦ",
        "\u0e30": "สระ อะ",
        "\u0e31": "ไม้หันอากาศ",
        "\u0e32": "สระ อา",
        "\u0e33": "สระ อำ",
        "\u0e34": "สระ อิ",
        "\u0e35": "สระ อี",
        "\u0e36": "สระ อึ",
        "\u0e37": "สระ อือ",
        "\u0e38": "สระ อุ",
        "\u0e39": "สระ อู",
        "\u0e40": "สระ เอ",
        "\u0e41": "สระ แอ",
        "\u0e42": "สระ โอ",
        "\u0e43": "สระ ใอ",
        "\u0e44": "สระ ไอ",
        "\u0e45": "ไม้ม้วน",
        "\u0e4d": "นฤคหิต",
        "\u0e47": "ไม้ไต่คู้",
        # Tone Marks
        "\u0e48": "ไม้เอก",
        "\u0e49": "ไม้โท",
        "\u0e4a": "ไม้ตรี",
        "\u0e4b": "ไม้จัตวา",
        # Other Signs
        "\u0e2f": "ไปยาลน้อย",
        "\u0e3a": "พินทุ",
        "\u0e46": "ไม้ยมก",
        "\u0e4c": "การันต์",
        "\u0e4e": "ยามักการ",
        # Punctuation
        "\u0e4f": "ฟองมัน",
        "\u0e5a": "อังคั่นคู่",
        "\u0e5b": "โคมุต",
        # Digits
        **{char: char for char in thai_digits},
        # Symbol
        "\u0e3f": "฿",
    }
)


def is_thai_char(ch: str) -> bool:
    """Check if a character is a Thai character.

    :param ch: input character
    :type ch: str
    :return: True if ch is a Thai character, otherwise False.
    :rtype: bool

    :Example:

        >>> from pythainlp.util import is_thai_char
        >>> is_thai_char("ก")  # THAI CHARACTER KO KAI
        True
        >>> is_thai_char("๕")  # THAI DIGIT FIVE
        True
    """
    ch_val = ord(ch)
    if _TH_FIRST_CHAR_ASCII <= ch_val <= _TH_LAST_CHAR_ASCII:
        return True
    return False


def isthaichar(ch: str) -> bool:
    """Check if a character is a Thai character.

    .. deprecated:: 5.3.2
        Use :func:`is_thai_char` instead.

    :param ch: input character
    :type ch: str
    :return: True if ch is a Thai character, otherwise False.
    :rtype: bool
    """
    warn_deprecation(
        "pythainlp.util.isthaichar",
        "pythainlp.util.is_thai_char",
        "5.3.2",
        "6.0",
    )
    return is_thai_char(ch)


def is_thai(text: str, ignore_chars: str = ".") -> bool:
    """Check if every character in a string is a Thai character.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to "."
    :type ignore_chars: str, optional
    :return: True if every character in the input string is Thai,
             otherwise False.
    :rtype: bool

    :Example:

        >>> from pythainlp.util import is_thai
        >>> is_thai("กาลเวลา")
        True
        >>> is_thai("กาลเวลา.")
        True
        >>> is_thai("กาล-เวลา")
        False
        >>> is_thai("กาล-เวลา +66", ignore_chars="01234567890+-., ")
        True

    """
    if not ignore_chars:
        ignore_chars = ""

    for ch in text:
        if ch not in ignore_chars and not is_thai_char(ch):
            return False
    return True


def isthai(text: str, ignore_chars: str = ".") -> bool:
    """Check if every character in a string is a Thai character.

    .. deprecated:: 5.3.2
        Use :func:`is_thai` instead.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to "."
    :type ignore_chars: str, optional
    :return: True if every character in the input string is Thai,
             otherwise False.
    :rtype: bool
    """
    warn_deprecation(
        "pythainlp.util.isthai",
        "pythainlp.util.is_thai",
        "5.3.2",
        "6.0",
    )
    return is_thai(text, ignore_chars)


def count_thai(text: str, ignore_chars: str = _DEFAULT_IGNORE_CHARS) -> float:
    """Find proportion of Thai characters in a given text.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to whitespace,\\
        digits, and punctuation marks.
    :type ignore_chars: str, optional
    :return: proportion of Thai characters in the text (percentage)
    :rtype: float

    :Example:

        >>> from pythainlp.util import count_thai
        >>> count_thai("ไทยเอ็นแอลพี 3.0")
        100.0
        >>> count_thai("PyThaiNLP 3.0")
        0.0
        >>> count_thai("ใช้งาน PyThaiNLP 3.0")
        40.0
        >>> count_thai("ใช้งาน PyThaiNLP 3.0", ignore_chars="")
        30.0
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
        elif is_thai_char(ch):
            num_thai += 1

    num_count = len(text) - num_ignore

    if num_count == 0:
        return 0.0

    return (num_thai / num_count) * 100


def countthai(text: str, ignore_chars: str = _DEFAULT_IGNORE_CHARS) -> float:
    """Find proportion of Thai characters in a given text.

    .. deprecated:: 5.3.2
        Use :func:`count_thai` instead.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to whitespace,\\
        digits, and punctuation marks.
    :type ignore_chars: str, optional
    :return: proportion of Thai characters in the text (percentage)
    :rtype: float
    """
    warn_deprecation(
        "pythainlp.util.countthai",
        "pythainlp.util.count_thai",
        "5.3.2",
        "6.0",
    )
    return count_thai(text, ignore_chars)


def display_thai_char(ch: str) -> str:
    """Prefix an underscore (_) to a high-position vowel or a tone mark,
    to ease readability.

    :param ch: input character
    :type ch: str
    :return: "_" + ch
    :rtype: str

    :Example:

        >>> from pythainlp.util import display_thai_char
        >>> display_thai_char("้")
        '_้'
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


def thai_word_tone_detector(word: Optional[str]) -> list[tuple[str, str]]:
    """Thai tone detector for word.

    It uses pythainlp.transliterate.pronunciate for converting word to\
        pronunciation.

    :param word: Thai word, or None
    :type word: str, optional
    :return: list of tuples (syllable, tone) for each syllable.
        Tone values: ``l`` (low), ``m`` (mid), ``h`` (high),
        ``r`` (rising), ``f`` (falling), or empty string
        if it cannot be detected.
        Returns ``[]`` if word is None or empty.
    :rtype: list[tuple[str, str]]

    :Example:

        >>> from pythainlp.util import thai_word_tone_detector
        >>> print(thai_word_tone_detector("คนดี"))
        [('คน', 'm'), ('ดี', 'm')]
        >>> print(thai_word_tone_detector("มือถือ"))
        [('มือ', 'm'), ('ถือ', 'r')]
        >>> print(thai_word_tone_detector(None))
        []
    """
    if not word:
        return []

    from ..transliterate import pronunciate
    from ..util.syllable import tone_detector

    _pronunciate = pronunciate(word).split("-")
    return [(i, tone_detector(i.replace("หฺ", "ห"))) for i in _pronunciate]


def count_thai_chars(text: str) -> dict[str, int]:
    """Count Thai characters by type.

    Count Thai characters by type: consonants, vowels, lead_vowels,
    follow_vowels, above_vowels, below_vowels, tonemarks, signs,
    thai_digits, punctuations, and non_thai.

    :param str text: input text
    :return: dict with counts of Thai characters by type
    :rtype: dict[str, int]

    :Example:

        >>> from pythainlp.util import count_thai_chars
        >>> count_thai_chars("ทดสอบภาษาไทย")  # doctest: +NORMALIZE_WHITESPACE
        {
        'vowels': 3,
        'lead_vowels': 1,
        'follow_vowels': 2,
        'above_vowels': 0,
        'below_vowels': 0,
        'consonants': 9,
        'tonemarks': 0,
        'signs': 0,
        'thai_digits': 0,
        'punctuations': 0,
        'non_thai': 0
        }
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


def analyze_thai_text(text: str) -> dict[str, int]:
    """Analyze Thai text and return a character count by descriptive name.

    Process the text character by character and map each Thai character
    to its descriptive name or to itself (for consonants and digits).

    :param str text: Thai text string to be analyzed
    :return: dict mapping character names to their count in the text
    :rtype: dict[str, int]

    :Example:

        >>> from pythainlp.util import analyze_thai_text
        >>> analyze_thai_text("คนดี")
        {'ค': 1, 'น': 1, 'ด': 1, 'สระ อี': 1}
        >>> analyze_thai_text("เล่น")
        {'สระ เอ': 1, 'ล': 1, 'ไม้เอก': 1, 'น': 1}

    """
    results: dict[str, int] = defaultdict(int)

    # Iterate over each character in the input string
    for char in text:
        # Check if the character is in our mapping
        if char in _THAI_CHAR_NAMES:
            name = _THAI_CHAR_NAMES[char]
            results[name] += 1
        else:
            # If the character is not a known Thai character, classify it as character
            results[char] += 1

    return dict(results)
