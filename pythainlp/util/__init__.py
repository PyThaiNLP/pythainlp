# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
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
    "find_keyword",
    "ipa_to_rtgs",
    "is_native_thai",
    "isthai",
    "isthaichar",
    "nectec_to_ipa",
    "normalize",
    "now_reign_year",
    "num_to_thaiword",
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
    "spell_words",
    "syllable_length",
    "syllable_open_close_detector",
    "text_to_arabic_digit",
    "text_to_num",
    "text_to_thai_digit",
    "thai_digit_to_arabic_digit",
    "thai_keyboard_dist",
    "thai_strptime",
    "thai_strftime",
    "thai_to_eng",
    "to_idna",
    "thai_word_tone_detector",
    "thaiword_to_date",
    "thaiword_to_num",
    "thaiword_to_time",
    "time_to_thaiword",
    "tis620_to_utf8",
    "tone_detector",
    "words_to_num",
]

from pythainlp.util.collate import collate
from pythainlp.util.date import (
    now_reign_year,
    reign_year_to_ad,
    thaiword_to_date,
    convert_years,
    thai_strptime,
)
from pythainlp.util.digitconv import (
    arabic_digit_to_thai_digit,
    digit_to_text,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
)
from pythainlp.util.keyboard import (
    eng_to_thai,
    thai_keyboard_dist,
    thai_to_eng,
)
from pythainlp.util.emojiconv import emoji_to_thai
from pythainlp.util.keywords import find_keyword, rank
from pythainlp.util.normalize import (
    normalize,
    maiyamok,
    remove_dangling,
    remove_dup_spaces,
    remove_repeat_vowels,
    remove_tonemark,
    remove_zw,
    reorder_vowels,
)
from pythainlp.util.remove_trailing_repeat_consonants import (
    remove_trailing_repeat_consonants,
)
from pythainlp.util.numtoword import bahttext, num_to_thaiword
from pythainlp.util.strftime import thai_strftime
from pythainlp.util.thai import (
    countthai,
    count_thai_chars,
    display_thai_char,
    isthai,
    isthaichar,
    thai_word_tone_detector,
)
from pythainlp.util.thaiwordcheck import is_native_thai
from pythainlp.util.time import thaiword_to_time, time_to_thaiword
from pythainlp.util.trie import Trie, dict_trie
from pythainlp.util.wordtonum import thaiword_to_num, text_to_num, words_to_num
from pythainlp.util.syllable import (
    sound_syllable,
    tone_detector,
    syllable_length,
    syllable_open_close_detector,
)
from pythainlp.util.phoneme import nectec_to_ipa, ipa_to_rtgs, remove_tone_ipa
from pythainlp.util.encoding import to_idna, tis620_to_utf8
from pythainlp.util import spell_words
from pythainlp.util.abbreviation import abbreviation_to_full_text
from pythainlp.util.pronounce import rhyme
