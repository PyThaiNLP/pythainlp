# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Utility functions, like date conversion and digit conversion
"""

__all__ = [
    "Trie",
    "abbreviation_to_full_text",
    "arabic_digit_to_thai_digit",
    "bahttext",
    "collate",
    "convert_years",
    "count_thai_chars",
    "countthai",
    "dict_trie",
    "digit_to_text",
    "display_thai_char",
    "emoji_to_thai",
    "eng_to_thai",
    "expand_maiyamok",
    "find_keyword",
    "ipa_to_rtgs",
    "is_native_thai",
    "isthai",
    "isthaichar",
    "longest_common_subsequence",
    "nectec_to_ipa",
    "normalize",
    "now_reign_year",
    "num_to_thaiword",
    "maiyamok",
    "rank",
    "reign_year_to_ad",
    "remove_dangling",
    "remove_dup_spaces",
    "remove_repeat_vowels",
    "remove_tone_ipa",
    "remove_tonemark",
    "remove_trailing_repeat_consonants",
    "remove_zw",
    "reorder_vowels",
    "rhyme",
    "sound_syllable",
    "spelling",
    "spell_words",
    "syllable_length",
    "syllable_open_close_detector",
    "text_to_arabic_digit",
    "text_to_num",
    "text_to_thai_digit",
    "th_zodiac",
    "thai_consonant_to_spelling",
    "thai_digit_to_arabic_digit",
    "thai_keyboard_dist",
    "thai_strptime",
    "thai_strftime",
    "thai_to_eng",
    "thai_word_tone_detector",
    "thaiword_to_date",
    "thaiword_to_num",
    "thaiword_to_time",
    "time_to_thaiword",
    "tis620_to_utf8",
    "to_idna",
    "to_lunar_date",
    "tone_detector",
    "tone_to_spelling",
    "words_to_num",
    "analyze_thai_text",
]

from pythainlp.util import spell_words
from pythainlp.util.abbreviation import abbreviation_to_full_text
from pythainlp.util.collate import collate
from pythainlp.util.date import (
    convert_years,
    now_reign_year,
    reign_year_to_ad,
    thai_strptime,
    thaiword_to_date,
)
from pythainlp.util.digitconv import (
    arabic_digit_to_thai_digit,
    digit_to_text,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
)
from pythainlp.util.emojiconv import emoji_to_thai
from pythainlp.util.encoding import tis620_to_utf8, to_idna
from pythainlp.util.keyboard import (
    eng_to_thai,
    thai_keyboard_dist,
    thai_to_eng,
)
from pythainlp.util.keywords import find_keyword, rank
from pythainlp.util.lcs import longest_common_subsequence
from pythainlp.util.normalize import (
    maiyamok,
    normalize,
    remove_dangling,
    remove_dup_spaces,
    remove_repeat_vowels,
    remove_tonemark,
    remove_zw,
    reorder_vowels,
    expand_maiyamok,
)
from pythainlp.util.numtoword import bahttext, num_to_thaiword
from pythainlp.util.phoneme import ipa_to_rtgs, nectec_to_ipa, remove_tone_ipa
from pythainlp.util.remove_trailing_repeat_consonants import (
    remove_trailing_repeat_consonants,
)
from pythainlp.util.strftime import thai_strftime
from pythainlp.util.thai import (
    count_thai_chars,
    countthai,
    display_thai_char,
    isthai,
    isthaichar,
    thai_word_tone_detector,
    analyze_thai_text,
)
from pythainlp.util.thai_lunar_date import th_zodiac, to_lunar_date
from pythainlp.util.thaiwordcheck import is_native_thai
from pythainlp.util.time import thaiword_to_time, time_to_thaiword
from pythainlp.util.trie import Trie, dict_trie
from pythainlp.util.wordtonum import text_to_num, thaiword_to_num, words_to_num

# sound_syllable and pronounce have to be imported last,
# to prevent circular import issues.
# Other imports should be above this line, sorted.
from pythainlp.util.syllable import (
    sound_syllable,
    syllable_length,
    syllable_open_close_detector,
    tone_detector,
)
from pythainlp.util.pronounce import (
    rhyme,
    spelling,
    tone_to_spelling,
    thai_consonant_to_spelling,
)
