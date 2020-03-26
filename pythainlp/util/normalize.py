# -*- coding: utf-8 -*-
"""
Text normalization
"""
import re
import warnings

from pythainlp import (
    thai_above_vowels,
    thai_below_vowels,
    thai_follow_vowels,
    thai_lead_vowels,
    thai_tonemarks,
)

_NO_REPEAT_CHARS = f"{thai_follow_vowels}{thai_lead_vowels}{thai_above_vowels}{thai_below_vowels}\u0e3a\u0e4c\u0e4d\u0e4e"
# VOWELS + Phinthu,Thanthakhat, Nikhahit, Yamakkan
_NORMALIZE_REPETITION = list(
    zip([ch + "+" for ch in _NO_REPEAT_CHARS], _NO_REPEAT_CHARS)
)

_NORMALIZE_REORDER = [
    ("\u0e40\u0e40", "\u0e41"),  # Sara E + Sara E -> Sara Ae
    (f"(\u0e4c)([{thai_above_vowels}{thai_below_vowels}])", "\\2\\1"),
    (
        f"\u0e4d([{thai_tonemarks}]*)\u0e32",
        "\\1\u0e33",
    ),  # Nikhahit + TONEMARK* + Sara Aa -> TONEMARK* + Sara Am
    (
        f"([{thai_follow_vowels}]+)([{thai_tonemarks}]+)",
        "\\2\\1",
    ),  # FOLLOWVOWEL+ + TONEMARK+ -> TONEMARK+ + FOLLOWVOWEL+
    (
        f"([{thai_tonemarks}]+)([{thai_above_vowels}{thai_below_vowels}]+)",
        "\\2\\1",
    ),  # TONEMARK+ + ABOVE/BELOWVOWEL+ -> ABOVE/BELOWVOWEL+ + TONEMARK+
]


def normalize(text: str) -> str:
    """
    This function normalize thai text with normalizing rules as follows:

        * Remove redundant vowels and tonemarks
        * Subsitute "เ" + "เ" with "แ"

    :param str text: thai text to be normalized
    :return: normalized Thai text according to the fules
    :rtype: str

    :Example:
    ::

        from pythainlp.util import normalize

        normalize('สระะน้ำ')
        # output: สระน้ำ

        normalize('เเปลก')
        # output: แปลก

        normalize('นานาาา')
        # output: นานา
    """
    for data in _NORMALIZE_REORDER:
        text = re.sub(data[0], data[1], text)
    for data in _NORMALIZE_REPETITION:
        text = re.sub(data[0], data[1], text)
    return text


def delete_tone(text: str) -> str:
    """
    This function removes Thai tonemarks from the text.
    There are 4 tonemarks indicating 4 tones as follows:

        * Down tone (Thai: ไม้เอก  _่ )
        * Falling tone  (Thai: ไม้โท  _้ )
        * High tone (Thai: ไม้ตรี  ​_๊ )
        * Rising tone (Thai: ไม้จัตวา _๋ )

    :param str text: text in Thai language
    :return: text without Thai tonemarks
    :rtype: str

    :Example:
    ::

        from pythainlp.util import delete_tone

        delete_tone('สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด')
        # output: สองพันหนึงรอยสีสิบเจ็ดลานสีแสนแปดหมืนสามพันหกรอยสีสิบเจ็ด
    """
    chars = [ch for ch in text if ch not in thai_tonemarks]
    return "".join(chars)


def deletetone(text: str) -> str:
    warnings.warn(
        "deletetone is deprecated, use delete_tone instead", DeprecationWarning
    )
    return delete_tone(text)
