# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Check if a word is a "native Thai word"

Adapted from
https://github.com/wannaphong/open-thai-nlp-document/blob/master/check_thai_word.md

References
- ทีมงานทรูปลูกปัญญา 2015. ลักษณะของคำไทยแท้ http://www.trueplookpanya.com/learning/detail/30589-043067
- วารุณี บำรุงรส 2010. คำไทยแท้ https://www.gotoknow.org/posts/377619
"""
import re

_THANTHAKHAT_CHAR = "\u0e4c"  # Thanthakhat (cancellation of sound)

# Non-native Thai characters
_TH_NON_NATIVE_CHARS = {
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
_TH_NATIVE_FINALS = {"ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"}

# Known native Thai words (exceptions)
_TH_NATIVE_WORDS = {
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

# Diphthong prefixes (can starts native Thai word)
_TH_PREFIX_DIPHTHONG = {"กะ", "กระ", "ปะ", "ประ"}

# Thai consonant filter
# O ANG (U+0E2D) is omitted, as it can be considered as vowel
_TH_CONSONANTS_PATTERN = re.compile(r"[ก-ฬฮ]", re.U)


def is_native_thai(word: str) -> bool:
    """
    Check if a word is an "native Thai word" (Thai: "คำไทยแท้")
    This function based on a simple heuristic algorithm
    and cannot be entirely reliable.

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

    English word::

        from pythainlp.util import is_native_thai

        is_native_thai("Avocado")
        # output: False

    Native Thai word::

        is_native_thai("มะม่วง")
        # output: True
        is_native_thai("ตะวัน")
        # output: True

    Non-native Thai word::

        is_native_thai("สามารถ")
        # output: False
        is_native_thai("อิสริยาภรณ์")
        # output: False
    """
    if not isinstance(word, str) or not word.strip():
        return False

    word = word.strip()

    # Known native Thai words (exceptions)
    if word in _TH_NATIVE_WORDS:
        return True

    # If a word contains non-Thai char, it is not a native Thai
    if any(ch in word for ch in _TH_NON_NATIVE_CHARS):
        return False

    # If does not contain any Thai consonants -> cannot be Thai
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
    # Prefix-sentitive tokenization is required in order to able to check this.
    if word in _TH_PREFIX_DIPHTHONG:
        return True

    return False
