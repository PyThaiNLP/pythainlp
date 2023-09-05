# -*- coding: utf-8 -*-
# PyThaiNLP: Thai Natural Language Processing in Python
#
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
#
# URL: <https://pythainlp.github.io/>
# For license information, see LICENSE
__version__ = "4.1.0beta4"

thai_consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"  # 44 chars

thai_vowels = (
    "\u0e24\u0e26\u0e30\u0e31\u0e32\u0e33\u0e34\u0e35\u0e36\u0e37"
    + "\u0e38\u0e39\u0e40\u0e41\u0e42\u0e43\u0e44\u0e45\u0e4d\u0e47"
)  # 20
thai_lead_vowels = "\u0e40\u0e41\u0e42\u0e43\u0e44"  # 5
thai_follow_vowels = "\u0e30\u0e32\u0e33\u0e45"  # 4
thai_above_vowels = "\u0e31\u0e34\u0e35\u0e36\u0e37\u0e4d\u0e47"  # 7
thai_below_vowels = "\u0e38\u0e39"  # 2

thai_tonemarks = "\u0e48\u0e49\u0e4a\u0e4b"  # 4

# Paiyannoi, Maiyamok, Phinthu, Thanthakhat, Nikhahit, Yamakkan:
# These signs can be part of a word
thai_signs = "\u0e2f\u0e3a\u0e46\u0e4c\u0e4d\u0e4e"  # 6 chars

# Any Thai character that can be part of a word
thai_letters = "".join(
    [thai_consonants, thai_vowels, thai_tonemarks, thai_signs]
)  # 74

# Fongman, Angkhankhu, Khomut:
# These characters are section markers
thai_punctuations = "\u0e4f\u0e5a\u0e5b"  # 3 chars

thai_digits = "๐๑๒๓๔๕๖๗๘๙"  # 10
thai_symbols = "\u0e3f"  # Thai Bath ฿

# All Thai characters that presented in Unicode
thai_characters = "".join(
    [thai_letters, thai_punctuations, thai_digits, thai_symbols]
)


from pythainlp.soundex import soundex
from pythainlp.spell import correct, spell
from pythainlp.tag import pos_tag
from pythainlp.tokenize import (
    Tokenizer,
    sent_tokenize,
    subword_tokenize,
    word_tokenize,
)
from pythainlp.transliterate import romanize, transliterate
from pythainlp.util import collate, thai_strftime
