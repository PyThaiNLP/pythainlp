# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text normalization."""

from __future__ import annotations

import re
from typing import Pattern, Union

from pythainlp import thai_above_vowels as above_v
from pythainlp import thai_below_vowels as below_v
from pythainlp import thai_consonants, thai_vowels
from pythainlp import thai_follow_vowels as follow_v
from pythainlp import thai_lead_vowels as lead_v
from pythainlp import thai_tonemarks as tonemarks
from pythainlp.tokenize import word_tokenize
from pythainlp.tools import warn_deprecation

_DANGLING_CHARS: str = f"{above_v}{below_v}{tonemarks}\u0e3a\u0e4c\u0e4d\u0e4e"
_RE_REMOVE_DANGLINGS: Pattern[str] = re.compile(f"^[{_DANGLING_CHARS}]+")
_RE_REMOVE_DANGLINGS_AFTER_SPACE: Pattern[str] = re.compile(
    f" +[{_DANGLING_CHARS}]+"
)

_ZERO_WIDTH_CHARS: str = "\u200b\u200c"  # ZWSP, ZWNJ

_REORDER_PAIRS: list[tuple[str, str]] = [
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
_NOREPEAT_CHARS: str = (
    f"{follow_v}{lead_v}{above_v}{below_v}\u0e3a\u0e4c\u0e4d\u0e4e"
)
_NOREPEAT_PAIRS: list[tuple[str, str]] = list(
    zip([f"({ch}[ ]*)+{ch}" for ch in _NOREPEAT_CHARS], _NOREPEAT_CHARS)
)

_RE_TONEMARKS: Pattern[str] = re.compile(f"[{tonemarks}]+")

_RE_REMOVE_NEWLINES: Pattern[str] = re.compile("[ \n]*\n[ \n]*")

# Remove single space before non-base characters, but only after a consonant
# that's not preceded by a vowel (to avoid breaking up complete words)
# This conservative approach fixes "พ ุ่ม" but preserves "ภาพ ุ่"
_RE_REMOVE_SPACES_BEFORE_NONBASE: Pattern[str] = re.compile(
    f"([{thai_consonants}])(?<![{thai_vowels}][{thai_consonants}]) ([{_DANGLING_CHARS}])"
)


def _last_char(
    matchobj: re.Match[str],
) -> str:  # to be used with _RE_NOREPEAT_TONEMARKS
    return matchobj.group(0)[-1]


def remove_dangling(text: str) -> str:
    """
    Remove Thai non-base characters at the beginning of text and after spaces.

    This is a common typo, especially in input fields of a form,
    as these non-base characters can be visually hidden from the user
    who may type them in accidentally.

    A character to be removed must meet both conditions:

        * it is a tone mark, above vowel, below vowel, or non-base sign
        * it is at the beginning of the text or after spaces

    :param str text: text to be normalized
    :return: text without dangling Thai characters at the beginning
        and after spaces
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_dangling
        >>> remove_dangling("๊ก")
        'ก'
        >>> remove_dangling("คำ ่ที่สอง")
        'คำ ที่สอง'
    """
    text = _RE_REMOVE_DANGLINGS.sub("", text)
    text = _RE_REMOVE_DANGLINGS_AFTER_SPACE.sub(" ", text)
    return text


def remove_dup_spaces(text: str) -> str:
    """
    Remove duplicate spaces.

    Replace multiple spaces with one space. Replace multiple newline
    characters and empty lines with one newline character.

    :param str text: text to be normalized
    :return: text without duplicated spaces and newlines
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_dup_spaces
        >>> remove_dup_spaces("ก    ข    ค")
        'ก ข ค'
    """
    while "  " in text:
        text = text.replace("  ", " ")
    text = _RE_REMOVE_NEWLINES.sub("\n", text)
    text = text.strip()
    return text


def remove_tonemark(text: str) -> str:
    """
    Remove all Thai tone marks from text.

    Thai script has four tone marks indicating four tones as follows:

        * Down tone (Thai: ไม้เอก  _่ )
        * Falling tone  (Thai: ไม้โท  _้ )
        * High tone (Thai: ไม้ตรี  _๊ )
        * Rising tone (Thai: ไม้จัตวา _๋ )

    Using a wrong tone mark is a common mistake in Thai writing.
    Text without tone marks can be used for approximate string matching.

    :param str text: text to be normalized
    :return: text without Thai tone marks
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_tonemark
        >>> remove_tonemark("สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด")
        'สองพันหนึงรอยสีสิบเจ็ดลานสีแสนแปดหมืนสามพันหกรอยสีสิบเจ็ด'
    """
    for ch in tonemarks:
        while ch in text:
            text = text.replace(ch, "")
    return text


def remove_zw(text: str) -> str:
    """
    Remove zero-width characters.

    These invisible characters may cause unexpected results from the
    user's point of view. Removing them makes string matching more robust.

    Characters to be removed:

        * Zero-width space (ZWSP)
        * Zero-width non-joiner (ZWNJ)

    :param str text: text to be normalized
    :return: text without zero-width characters
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_zw
        >>> remove_zw("สวัสดี\u200bครับ")
        'สวัสดีครับ'
        >>> remove_zw("ภาษา\u200cไทย")
        'ภาษาไทย'
    """
    for ch in _ZERO_WIDTH_CHARS:
        while ch in text:
            text = text.replace(ch, "")

    return text


def remove_spaces_before_marks(text: str) -> str:
    """
    Remove spaces before Thai tone marks and non-base characters.

    Spaces before tone marks, above vowels, below vowels, and other
    non-base characters are often unintentional typos. This function
    removes such spaces to normalize the text.

    :param str text: text to be normalized
    :return: text without spaces before Thai tone marks and
        non-base characters
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_spaces_before_marks
        >>> remove_spaces_before_marks("พ ุ่มดอกไม้")
        'พุ่มดอกไม้'
    """
    return _RE_REMOVE_SPACES_BEFORE_NONBASE.sub(r"\1\2", text)


def reorder_vowels(text: str) -> str:
    """
    Reorder vowels and tone marks to the standard logical order.

    This function reorders or transforms characters in text
    according to these rules:

        * Sara E + Sara E -> Sara Ae
        * Nikhahit + Sara Aa -> Sara Am
        * tone mark + non-base vowel -> non-base vowel + tone mark
        * follow vowel + tone mark -> tone mark + follow vowel

    :param str text: text to be normalized
    :return: text with vowels and tone marks in the standard logical order
    :rtype: str

    :Example:

        >>> from pythainlp.util import reorder_vowels
        >>> reorder_vowels("เเปลก")  # two Sara E become Sara Ae
        'แปลก'
        >>> reorder_vowels("ก้ำ")  # reorder tone marks and vowels
        'ก้ำ'
    """
    for pair in _REORDER_PAIRS:
        text = re.sub(pair[0], pair[1], text)

    return text


def remove_repeat_vowels(text: str) -> str:
    """
    Remove repeating vowels, tone marks, and signs.

    This function calls :func:`reorder_vowels` first, so that
    a double Sara E becomes Sara Ae and is not removed.

    :param str text: text to be normalized
    :return: text without repeating Thai vowels, tone marks, and signs
    :rtype: str

    :Example:

        >>> from pythainlp.util import remove_repeat_vowels
        >>> remove_repeat_vowels("นานาาา")
        'นานา'
        >>> remove_repeat_vowels("ดีีีี")
        'ดี'
    """
    text = reorder_vowels(text)
    for pair in _NOREPEAT_PAIRS:
        text = re.sub(pair[0], pair[1], text)

    # remove repeating tone marks, use last tone mark
    text = _RE_TONEMARKS.sub(_last_char, text)

    return text


def normalize(text: str) -> str:
    """
    Normalize and clean Thai text.

    This function applies these rules:

        * Remove zero-width spaces
        * Remove duplicate spaces
        * Remove spaces before tone marks and non-base characters
        * Reorder tone marks and vowels to standard order/spelling
        * Remove duplicate vowels and signs
        * Remove duplicate tone marks
        * Remove dangling non-base characters at the beginning of text

    This function calls :func:`remove_zw`, :func:`remove_dup_spaces`,
    :func:`remove_spaces_before_marks`, :func:`remove_repeat_vowels`,
    and :func:`remove_dangling`, in that order.

    To customize the selection or the order of rules,
    call those functions separately.

    Note: for Unicode normalization, see :func:`unicodedata.normalize`.

    :param str text: text to be normalized
    :return: normalized text
    :rtype: str

    :Example:

        >>> from pythainlp.util import normalize
        >>> normalize("เเปลก")  # starts with two Sara E
        'แปลก'
        >>> normalize("นานาาา")
        'นานา'
    """
    text = remove_zw(text)
    text = remove_dup_spaces(text)
    text = remove_spaces_before_marks(text)
    text = remove_repeat_vowels(text)
    text = remove_dangling(text)

    return text


_MAIYAMOK: str = "ๆ"
_RE_MAIYAMOK: Pattern[str] = re.compile(f"({_MAIYAMOK})")


def _split_maiyamok(sent: list[str]) -> list[str]:
    """
    Split Maiyamok that is attached to other text.

    Examples of such text are "นกๆๆ", "นกๆ ๆ", and "นกๆคน".
    """
    tokens: list[str] = []
    for token in sent:
        tokens.extend(filter(None, _RE_MAIYAMOK.split(token)))
    return tokens


def expand_maiyamok(sent: Union[str, list[str]]) -> list[str]:
    """
    Expand Maiyamok.

    Maiyamok (ๆ) (Unicode U+0E46) is a Thai character indicating word
    repetition. This function preprocesses Thai text by replacing
    Maiyamok with the repeated word.

    :param Union[str, list[str]] sent: sentence, as text or list of words
    :return: list of words
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util import expand_maiyamok
        >>> expand_maiyamok("คนๆนก")
        ['คน', 'คน', 'นก']
    """
    if isinstance(sent, str):
        sent = word_tokenize(sent)

    output_toks: list[str] = []
    yamok_count = 0
    for tok in reversed(_split_maiyamok(sent)):  # do it backward
        if tok == _MAIYAMOK:
            yamok_count += 1
        elif yamok_count == 0:
            output_toks.append(tok)
        elif not tok.isspace():  # drop space before Maiyamok
            output_toks.extend([tok] * (yamok_count + 1))
            yamok_count = 0

    return output_toks[::-1]


def maiyamok(sent: Union[str, list[str]]) -> list[str]:
    """
    Expand Maiyamok.

    .. deprecated:: 5.0.5
        Use :func:`expand_maiyamok` instead.

    Maiyamok (ๆ) (Unicode U+0E46) is a Thai character indicating word
    repetition. This function preprocesses Thai text by replacing
    Maiyamok with the repeated word.

    :param Union[str, list[str]] sent: sentence, as text or list of words
    :return: list of words
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util import maiyamok

        >>> maiyamok("คนๆนก")
        ['คน', 'คน', 'นก']
    """
    warn_deprecation(
        "pythainlp.util.maiyamok",
        "pythainlp.util.expand_maiyamok",
        "5.0.5",
        "5.2",
    )
    return expand_maiyamok(sent)
