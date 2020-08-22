# -*- coding: utf-8 -*-
"""
Utility functions, like date conversion and digit conversion
"""

__all__ = [
    "Trie",
    "arabic_digit_to_thai_digit",
    "bahttext",
    "collate",
    "countthai",
    "delete_tone",
    "dict_trie",
    "digit_to_text",
    "display_thai_char",
    "eng_to_thai",
    "find_keyword",
    "is_native_thai",
    "isthai",
    "isthaichar",
    "normalize",
    "now_reign_year",
    "num_to_thaiword",
    "rank",
    "reign_year_to_ad",
    "remove_dangling",
    "remove_dup_spaces",
    "remove_repeat_vowels",
    "remove_tonemark",
    "remove_zw",
    "reorder_vowels",
    "text_to_arabic_digit",
    "text_to_thai_digit",
    "thai_digit_to_arabic_digit",
    "thai_strftime",
    "thai_time",
    "thai_to_eng",
    "thaiword_to_date",
    "thaiword_to_num",
    "thaiword_to_time",
    "time_to_thaiword",
]

from pythainlp.util.collate import collate
from pythainlp.util.date import (
    now_reign_year,
    reign_year_to_ad,
    thaiword_to_date,
)
from pythainlp.util.digitconv import (
    arabic_digit_to_thai_digit,
    digit_to_text,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
)
from pythainlp.util.keyboard import eng_to_thai, thai_to_eng
from pythainlp.util.keywords import find_keyword, rank
from pythainlp.util.normalize import (
    delete_tone,
    normalize,
    remove_dangling,
    remove_dup_spaces,
    remove_repeat_vowels,
    remove_tonemark,
    remove_zw,
    reorder_vowels,
)
from pythainlp.util.numtoword import bahttext, num_to_thaiword
from pythainlp.util.strftime import thai_strftime
from pythainlp.util.thai import countthai, isthai, isthaichar, \
    display_thai_char
from pythainlp.util.thaiwordcheck import is_native_thai
from pythainlp.util.time import thai_time, thaiword_to_time, time_to_thaiword
from pythainlp.util.trie import Trie, dict_trie
from pythainlp.util.wordtonum import thaiword_to_num
