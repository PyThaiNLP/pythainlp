# -*- coding: utf-8 -*-
"""
Utility functions, like date conversion and digit conversion
"""

__all__ = [
    "arabic_digit_to_thai_digit",
    "bahttext",
    "collate",
    "countthai",
    "delete_tone",
    "digit_to_text",
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
    "text_to_arabic_digit",
    "text_to_thai_digit",
    "thai_digit_to_arabic_digit",
    "thai_strftime",
    "thai_time",
    "thai_time2time",
    "thai_to_eng",
    "thaiword_to_num",
    "thai_day2datetime",
]


from .collate import collate
from .date import (
    now_reign_year,
    reign_year_to_ad,
    thai_strftime,
    thai_day2datetime,
)
from .digitconv import (
    arabic_digit_to_thai_digit,
    digit_to_text,
    text_to_arabic_digit,
    text_to_thai_digit,
    thai_digit_to_arabic_digit,
)
from .keyboard import eng_to_thai, thai_to_eng
from .keywords import find_keyword, rank
from .normalize import delete_tone, normalize
from .numtoword import bahttext, num_to_thaiword
from .thai import countthai, isthai, isthaichar
from .time import thai_time, thai_time2time
from .thaiwordcheck import is_native_thai
from .wordtonum import thaiword_to_num
