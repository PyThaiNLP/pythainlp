# -*- coding: utf-8 -*-
"""
Text normalization
"""
import re
import warnings

from pythainlp import thai_above_vowels as above_v
from pythainlp import thai_below_vowels as below_v
from pythainlp import thai_follow_vowels as follow_v
from pythainlp import thai_lead_vowels as lead_v
from pythainlp import thai_tonemarks as tonemarks


# VOWELS + Phinthu,Thanthakhat, Nikhahit, Yamakkan
_NO_REPEAT_CHARS = (
    f"{follow_v}{lead_v}{above_v}{below_v}\u0e3a\u0e4c\u0e4d\u0e4e"
)
_NORMALIZE_REPETITION = list(
    zip([ch + "+" for ch in _NO_REPEAT_CHARS], _NO_REPEAT_CHARS)
)

_NORMALIZE_REORDER = [
    ("\u0e40\u0e40", "\u0e41"),  # Sara E + Sara E -> Sara Ae
    (
        f"([{tonemarks}\u0e4c]+)([{above_v}{below_v}]+)",
        "\\2\\1",
    ),  # TONE/Thanthakhat+ + A/BVOWELV+ -> A/BVOWEL+ + TONE/Thanthakhat+
    (
        f"\u0e4d([{tonemarks}]*)\u0e32",
        "\\1\u0e33",
    ),  # Nikhahit + TONEMARK* + Sara Aa -> TONEMARK* + Sara Am
    (
        f"([{follow_v}]+)([{tonemarks}]+)",
        "\\2\\1",
    ),  # FOLLOWVOWEL+ + TONEMARK+ -> TONEMARK+ + FOLLOWVOWEL+
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
    chars = [ch for ch in text if ch not in tonemarks]
    return "".join(chars)
