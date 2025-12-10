# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
__version__ = "5.2.0"

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

# All Thai characters that are presented in Unicode
thai_characters = "".join(
    [thai_letters, thai_punctuations, thai_digits, thai_symbols]
)
# Thai pangram by Sungsit Sawaiwan
# CC BY-SA License
# Source: https://fontuni.com/articles/2015-07-12-thai-poetgram.html
thai_pangram = """กีฬาบังลังก์ ฿๑,๒๓๔,๕๖๗,๘๙๐
๏ จับฅอคนบั่นต้อง 	อาญา
ขุดฆ่าโคตรฃัตติยา 	ซ่านม้วย
ธรรมฤๅผ่อนรักษา 	ใจชั่ว โฉดแฮ
สืบอยู่เต็มศึกด้วย 	ฝุ่นฟ้ากีฬา กามฦๅ ฯ
๏ กตัญญูไป่พร้อม 	ปฐมฌาน
เกมส๎วัฒน์ปฏิภาณ 	ห่อนล้ำ
ทฤษฎีถ่อยๆ สังหาร 	เกณฑ์โทษ
โกรธจี๊ดจ๋อยจ่มถ้ำ 	อยู่เฝ้า “อตฺตา” ๚ะ๛
๑๒ กรกฎาคม ๒๕๕๘"""

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
