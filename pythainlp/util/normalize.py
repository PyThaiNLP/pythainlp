# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Text normalization
"""
import re
from typing import List, Union

from pythainlp import thai_above_vowels as above_v
from pythainlp import thai_below_vowels as below_v
from pythainlp import thai_follow_vowels as follow_v
from pythainlp import thai_lead_vowels as lead_v
from pythainlp import thai_tonemarks as tonemarks
from pythainlp.tokenize import word_tokenize


_DANGLING_CHARS = f"{above_v}{below_v}{tonemarks}\u0e3a\u0e4c\u0e4d\u0e4e"
_RE_REMOVE_DANGLINGS = re.compile(f"^[{_DANGLING_CHARS}]+")

_ZERO_WIDTH_CHARS = "\u200b\u200c"  # ZWSP, ZWNJ

_REORDER_PAIRS = [
    ("\u0e40\u0e40", "\u0e41"),  # Sara E + Sara E -> Sara Ae
    (
        f"([{tonemarks}\u0e4c]+)([{above_v}{below_v}]+)",
        "\\2\\1",
    ),  # TONE/Thanthakhat + ABV/BLW VOWEL -> ABV/BLW VOWEL + TONE/Thanthakhat
    (
        f"\u0e4d([{tonemarks}]*)\u0e32",
        "\\1\u0e33",
    ),  # Nikhahit + TONEMARK + Sara Aa -> TONEMARK + Sara Am
    (
        f"([{follow_v}]+)([{tonemarks}]+)",
        "\\2\\1",
    ),  # FOLLOW VOWEL + TONEMARK+ -> TONEMARK + FOLLOW VOWEL
    ("([^\u0e24\u0e26])\u0e45", "\\1\u0e32"),  # Lakkhangyao -> Sara Aa
]

# VOWELS + Phinthu, Thanthakhat, Nikhahit, Yamakkan
_NOREPEAT_CHARS = (
    f"{follow_v}{lead_v}{above_v}{below_v}\u0e3a\u0e4c\u0e4d\u0e4e"
)
_NOREPEAT_PAIRS = list(
    zip([f"({ch}[ ]*)+{ch}" for ch in _NOREPEAT_CHARS], _NOREPEAT_CHARS)
)

_RE_TONEMARKS = re.compile(f"[{tonemarks}]+")

_RE_REMOVE_NEWLINES = re.compile("[ \n]*\n[ \n]*")


def _last_char(matchobj):  # to be used with _RE_NOREPEAT_TONEMARKS
    return matchobj.group(0)[-1]


def remove_dangling(text: str) -> str:
    """
    Remove Thai non-base characters at the beginning of text.

    This is a common "typo", especially for input field in a form,
    as these non-base characters can be visually hidden from user
    who may accidentally typed them in.

    A character to be removed should be both:

        * tone mark, above vowel, below vowel, or non-base sign AND
        * located at the beginning of the text

    :param str text: input text
    :return: text without dangling Thai characters at the beginning
    :rtype: str

    :Example:
    ::

        from pythainlp.util import remove_dangling

        remove_dangling('๊ก')
        # output: 'ก'
    """
    return _RE_REMOVE_DANGLINGS.sub("", text)


def remove_dup_spaces(text: str) -> str:
    """
    Remove duplicate spaces. Replace multiple spaces with one space.

    Multiple newline characters and empty lines will be replaced
    with one newline character.

    :param str text: input text
    :return: text without duplicated spaces and newlines
    :rtype: str

    :Example:
    ::

        from pythainlp.util import remove_dup_spaces

        remove_dup_spaces('ก    ข    ค')
        # output: 'ก ข ค'
    """
    while "  " in text:
        text = text.replace("  ", " ")
    text = _RE_REMOVE_NEWLINES.sub("\n", text)
    text = text.strip()
    return text


def remove_tonemark(text: str) -> str:
    """
    Remove all Thai tone marks from the text.

    Thai script has four tone marks indicating four tones as follows:

        * Down tone (Thai: ไม้เอก  _่ )
        * Falling tone  (Thai: ไม้โท  _้ )
        * High tone (Thai: ไม้ตรี  _๊ )
        * Rising tone (Thai: ไม้จัตวา _๋ )

    Putting wrong tone mark is a common mistake in Thai writing.
    By removing tone marks from the string, it could be used to
    for a approximate string matching.

    :param str text: input text
    :return: text without Thai tone marks
    :rtype: str

    :Example:
    ::

        from pythainlp.util import remove_tonemark

        remove_tonemark('สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด')
        # output: สองพันหนึงรอยสีสิบเจ็ดลานสีแสนแปดหมืนสามพันหกรอยสีสิบเจ็ด
    """
    for ch in tonemarks:
        while ch in text:
            text = text.replace(ch, "")
    return text


def remove_zw(text: str) -> str:
    """
    Remove zero-width characters.

    These non-visible characters may cause unexpected result from the
    user's point of view. Removing them can make string matching more robust.

    Characters to be removed:

        * Zero-width space (ZWSP)
        * Zero-width non-joiner (ZWJP)

    :param str text: input text
    :return: text without zero-width characters
    :rtype: str
    """
    for ch in _ZERO_WIDTH_CHARS:
        while ch in text:
            text = text.replace(ch, "")

    return text


def reorder_vowels(text: str) -> str:
    """
    Reorder vowels and tone marks to the standard logical order/spelling.

    Characters in input text will be reordered/transformed,
    according to these rules:

        * Sara E + Sara E -> Sara Ae
        * Nikhahit + Sara Aa -> Sara Am
        * tone mark + non-base vowel -> non-base vowel + tone mark
        * follow vowel + tone mark -> tone mark + follow vowel

    :param str text: input text
    :return: text with vowels and tone marks in the standard logical order
    :rtype: str
    """
    for pair in _REORDER_PAIRS:
        text = re.sub(pair[0], pair[1], text)

    return text


def remove_repeat_vowels(text: str) -> str:
    """
    Remove repeating vowels, tone marks, and signs.

    This function will call reorder_vowels() first, to make sure that
    double Sara E will be converted to Sara Ae and not be removed.

    :param str text: input text
    :return: text without repeating Thai vowels, tone marks, and signs
    :rtype: str
    """
    text = reorder_vowels(text)
    for pair in _NOREPEAT_PAIRS:
        text = re.sub(pair[0], pair[1], text)

    # remove repeating tone marks, use last tone mark
    text = _RE_TONEMARKS.sub(_last_char, text)

    return text


def normalize(text: str) -> str:
    """
    Normalize and clean Thai text with normalizing rules as follows:

        * Remove zero-width spaces
        * Remove duplicate spaces
        * Reorder tone marks and vowels to standard order/spelling
        * Remove duplicate vowels and signs
        * Remove duplicate tone marks
        * Remove dangling non-base characters at the beginning of text

    normalize() simply call remove_zw(), remove_dup_spaces(),
    remove_repeat_vowels(), and remove_dangling(), in that order.

    If a user wants to customize the selection or the order of rules
    to be applied, they can choose to call those functions by themselves.

    Note: for Unicode normalization, see unicodedata.normalize().

    :param str text: input text
    :return: normalized text according to the rules
    :rtype: str

    :Example:
    ::

        from pythainlp.util import normalize

        normalize('เเปลก')  # starts with two Sara E
        # output: แปลก

        normalize('นานาาา')
        # output: นานา
    """
    text = remove_zw(text)
    text = remove_dup_spaces(text)
    text = remove_repeat_vowels(text)
    text = remove_dangling(text)

    return text


def maiyamok(sent: Union[str, List[str]]) -> List[str]:
    """
    Thai MaiYaMok

    MaiYaMok (ๆ) is the mark of duplicate word in Thai language.
    This function is preprocessing MaiYaMok in Thai sentence.

    :param Union[str, List[str]] sent: input sentence (list or str)
    :return: list of words
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util import maiyamok

        maiyamok("เด็กๆชอบไปโรงเรียน")
        # output: ['เด็ก', 'เด็ก', 'ชอบ', 'ไป', 'โรงเรียน']

        maiyamok(["ทำไม","คน","ดี"," ","ๆ","ๆ"," ","ถึง","ทำ","ไม่ได้"])
        # output: ['ทำไม', 'คน', 'ดี', 'ดี', 'ดี', ' ', 'ถึง', 'ทำ', 'ไม่ได้']
    """
    if isinstance(sent, str):
        sent = word_tokenize(sent)
    _list_word = []
    i = 0
    for j, text in enumerate(sent):
        if text.isspace() and "ๆ" in sent[j + 1]:
            continue
        if " ๆ" in text:
            text = text.replace(" ๆ", "ๆ")
        if "ๆ" == text:
            text = _list_word[i - 1]
        elif "ๆ" in text:
            count = text.count("ๆ")
            text = _list_word[i - 1]
            for _ in range(count):
                _list_word.append(text)
            i += 1
            continue
        _list_word.append(text)
        i += 1
    return _list_word
