# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Check if a word is a "native Thai word"

Adapted from
https://github.com/wannaphong/open-thai-nlp-document/blob/master/check_thai_word.md

References
----------
- ทีมงานทรูปลูกปัญญา 2015. ลักษณะของคำไทยแท้ \
    https://www.trueplookpanya.com/learning/detail/30589-043067
- วารุณี บำรุงรส 2010. คำไทยแท้ https://www.gotoknow.org/posts/377619

"""

from __future__ import annotations

import re

_THANTHAKHAT_CHAR: str = "\u0e4c"  # Thanthakhat (cancellation of sound)

# Non-native Thai characters
_TH_NON_NATIVE_CHARS: set[str] = {
    "ฆ",
    "ณ",
    "ฌ",
    "ฎ",
    "ฏ",
    "ฐ",
    "ฑ",
    "ฒ",
    "ธ",
    "ศ",
    "ษ",
    "ฬ",
    _THANTHAKHAT_CHAR,
}

# Native Thai final consonants
_TH_NATIVE_FINALS: set[str] = {"ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"}

# Known native Thai words (exceptions)
_TH_NATIVE_WORDS: set[str] = {
    "ฆ่า",
    "เฆี่ยน",
    "ศึก",
    "ศอก",
    "เศิก",
    "เศร้า",
    "ธ",
    "ณ",
    "ฯพณฯ",
    "ใหญ่",
    "หญ้า",
    "ควาย",
    "ความ",
    "กริ่งเกรง",
    "ผลิ",
}

# Diphthong prefixes (can start native Thai word)
_TH_PREFIX_DIPHTHONG: set[str] = {"กะ", "กระ", "ปะ", "ประ"}

# Thai consonant filter
# O ANG (U+0E2D) is omitted, as it can be considered as vowel
_TH_CONSONANTS_PATTERN: re.Pattern[str] = re.compile(r"[ก-ฬฮ]", re.U)


def is_native_thai(word: str) -> bool:
    """Check if a word is an "native Thai word" (Thai: "คำไทยแท้")
    This function is based on a simple heuristic algorithm
    and cannot be entirely reliable.

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

        >>> from pythainlp.morpheme import is_native_thai
        >>> is_native_thai("Avocado")
        False
        >>> is_native_thai("มะม่วง")
        True
        >>> is_native_thai("ตะวัน")
        True
        >>> is_native_thai("สามารถ")
        False
        >>> is_native_thai("อิสริยาภรณ์")
        False
    """
    if not isinstance(word, str) or not word.strip():
        return False

    word = word.strip()

    # Known native Thai words (exceptions)
    if word in _TH_NATIVE_WORDS:
        return True

    # If a word contains non-Thai chars, it is not a native Thai
    if any(ch in word for ch in _TH_NON_NATIVE_CHARS):
        return False

    # If it does not contain any Thai consonants -> it cannot be Thai
    chs = re.findall(_TH_CONSONANTS_PATTERN, word)
    if not chs:
        return False

    # If there's only one Thai consonant -> it can be a native Thai
    if len(chs) == 1:
        return True

    # If a word ends with native final, it can be a native Thai
    if word[-1] in _TH_NATIVE_FINALS:
        return True

    # Note: This will not work, as it check the whole word, not the prefix.
    # Prefix-sensitive tokenization is required in order to be able to check this.
    if word in _TH_PREFIX_DIPHTHONG:
        return True

    return False
