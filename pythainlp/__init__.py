# -*- coding: utf-8 -*-

__version__ = "2.0.1"

thai_consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"  # 44 chars
thai_vowels = "ฤฦะ\u0e31าำ\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39เแโใไ\u0e45\u0e47"  # 19
thai_tonemarks = "\u0e48\u0e49\u0e4a\u0e4b"  # 4

# Thai Characters: Paiyannoi, Maiyamok, Phinthu, Thanthakhat, Nikhahit, Yamakkan
# These signs can be part of a word
thai_signs = "ฯๆ\u0e3a\u0e4c\u0e4d\u0e4e"  # 6 chars

# Any Thai character that can be part of a word
thai_letters = "".join([thai_consonants, thai_vowels, thai_tonemarks, thai_signs])  # 73

# Thai Characters Fongman, Angkhankhu, Khomut
# These characters are section markers
thai_punctuations = "\u0e4f\u0e5a\u0e5b"  # 3 chars

thai_digits = "๐๑๒๓๔๕๖๗๘๙"  # 10
thai_symbols = "฿"

# All Thai characters that presented in Unicode
thai_characters = "".join([thai_letters, thai_punctuations, thai_digits, thai_symbols])


from pythainlp.soundex import soundex
from pythainlp.spell import correct, spell
from pythainlp.tag import pos_tag
from pythainlp.tokenize import sent_tokenize, tcc, word_tokenize, Tokenizer
from pythainlp.transliterate import romanize, transliterate
from pythainlp.util import collate, thai_strftime
