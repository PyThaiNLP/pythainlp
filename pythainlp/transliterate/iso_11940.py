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
Transliterating Thai text with ISO 11940

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
    "ๆ": "«",
    "ฯ": "ǂ",
    "๏": "§",
    "ฯ": "ǀ",
    "๚": "ǁ",
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
_list_k = _all_dict.keys()


def transliterate(word: str) -> str:
    """
    Use ISO 11940 for transliteration
    :param str text: Thai text to be transliterated.
    :return: A string of IPA indicating how the text should be pronounced.
    """
    _new = ""
    for i in word:
        if i in _list_k:
            _new += _all_dict[i]
        else:
            _new += i
    return _new
