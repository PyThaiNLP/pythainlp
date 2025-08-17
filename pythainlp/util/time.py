# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Spell out time as Thai words.

Convert time string or time object to Thai words.
"""
from datetime import datetime, time
from typing import Union

from pythainlp.tokenize import Tokenizer
from pythainlp.util.numtoword import num_to_thaiword
from pythainlp.util.wordtonum import thaiword_to_num

_TIME_FORMAT_WITH_SEC = "%H:%M:%S"
_TIME_FORMAT_WITHOUT_SEC = "%H:%M"
_DICT_THAI_TIME = {
    "ศูนย์": 0,
    "หนึ่ง": 1,
    "สอง": 2,
    "ยี่": 2,
    "สาม": 3,
    "สี่": 4,
    "ห้า": 5,
    "หก": 6,
    "เจ็ด": 7,
    "แปด": 8,
    "เก้า": 9,
    "สิบ": 10,
    "เอ็ด": 1,
    # set the value of the time unit
    "โมงเช้า": 6,  # start counting at 7:00 a.m.
    "โมงเย็น": 13,
    "บ่าย": 13,
    "บ่ายโมง": 13,
    "ตี": 0,
    "เที่ยงวัน": 12,
    "เที่ยงคืน": 0,
    "เที่ยง": 12,
    "ทุ่ม": 18,
    "นาฬิกา": 0,
    "ครึ่ง": 30,
}
_THAI_TIME_CUT = Tokenizer(
    custom_dict=list(_DICT_THAI_TIME.keys()), engine="newmm"
)
_THAI_TIME_AFFIX = [
    "โมงเช้า",
    "บ่ายโมง",
    "โมงเย็น",
    "โมง",
    "นาฬิกา",
    "ทุ่ม",
    "ตี",
    "เที่ยงคืน",
    "เที่ยงวัน",
    "เที่ยง",
]


def _format_6h(h: int) -> str:
    """Thai time (6-hour clock)."""
    text = ""

    if h == 0:
        text += "เที่ยงคืน"
    elif h < 7:
        text += "ตี" + num_to_thaiword(h)
    elif h < 12:
        text += num_to_thaiword(h - 6) + "โมงเช้า"
    elif h == 12:
        text += "เที่ยง"
    elif h < 18:
        if h == 13:
            text += "บ่ายโมง"
        else:
            text += "บ่าย" + num_to_thaiword(h - 12) + "โมง"
    elif h == 18:
        text += "หกโมงเย็น"
    else:
        text += num_to_thaiword(h - 18) + "ทุ่ม"

    return text


def _format_m6h(h: int) -> str:
    """Thai time (modified 6-hour clock)."""
    text = ""

    if h == 0:
        text += "เที่ยงคืน"
    elif h < 6:
        text += "ตี" + num_to_thaiword(h)
    elif h < 12:
        text += num_to_thaiword(h) + "โมง"
    elif h == 12:
        text += "เที่ยง"
    elif h < 19:
        text += num_to_thaiword(h - 12) + "โมง"
    else:
        text += num_to_thaiword(h - 18) + "ทุ่ม"

    return text


def _format_24h(h: int) -> str:
    """Thai time (24-hour clock)."""
    text = num_to_thaiword(h) + "นาฬิกา"
    return text


def _format(
    h: int,
    m: int,
    s: int,
    fmt: str = "24h",
    precision: Union[str, None] = None,
) -> str:
    text = ""
    if fmt == "6h":
        text = _format_6h(h)
    elif fmt == "m6h":
        text = _format_m6h(h)
    elif fmt == "24h":
        text = _format_24h(h)
    else:
        raise NotImplementedError(f"Time format not supported: {fmt}")

    if precision in ("m", "s"):
        if m == 30 and (s == 0 or precision == "m") and (fmt in ("6h", "m6h")):
            text += "ครึ่ง"
        else:
            text += num_to_thaiword(m) + "นาที"
            if precision == "s":
                text += num_to_thaiword(s) + "วินาที"
    else:
        if m:
            if m == 30 and s == 0 and (fmt in ("6h", "m6h")):
                text += "ครึ่ง"
            else:
                text += num_to_thaiword(m) + "นาที"
        if s:
            text += num_to_thaiword(s) + "วินาที"

    return text


def time_to_thaiword(
    time_data: Union[time, datetime, str],
    fmt: str = "24h",
    precision: Union[str, None] = None,
) -> str:
    """
    Spell out time as Thai words.

    :param str time_data: time input, can be a datetime.time object \
        or a datetime.datetime object \
        or a string (in H:M or H:M:S format, using 24-hour clock)
    :param str fmt: time output format
        * *24h* - 24-hour clock (default)
        * *6h* - 6-hour clock
        * *m6h* - Modified 6-hour clock
    :param str precision: precision of the spell out time
        * *m* - always spell out at minute level
        * *s* - always spell out at second level
        * None - spell out only non-zero parts
    :return: Time spelled out as Thai words
    :rtype: str

    :Example:
    ::

        time_to_thaiword("8:17")
        # output:
        # แปดนาฬิกาสิบเจ็ดนาที

        time_to_thaiword("8:17", "6h")
        # output:
        # สองโมงเช้าสิบเจ็ดนาที

        time_to_thaiword("8:17", "m6h")
        # output:
        # แปดโมงสิบเจ็ดนาที

        time_to_thaiword("18:30", fmt="m6h")
        # output:
        # หกโมงครึ่ง

        time_to_thaiword(datetime.time(12, 3, 0))
        # output:
        # สิบสองนาฬิกาสามนาที

        time_to_thaiword(datetime.time(12, 3, 0), precision="s")
        # output:
        # สิบสองนาฬิกาสามนาทีศูนย์วินาที
    """
    _time = None

    if isinstance(time_data, (time, datetime)):
        _time = time_data
    else:
        if not isinstance(time_data, str):
            raise TypeError(
                "Time input must be a datetime.time object, "
                "a datetime.datetime object, or a string."
            )

        if not time_data:
            raise ValueError("Time string cannot be empty.")

        try:
            _time = datetime.strptime(time_data, _TIME_FORMAT_WITH_SEC)
        except ValueError:
            try:
                _time = datetime.strptime(time_data, _TIME_FORMAT_WITHOUT_SEC)
            except ValueError:
                pass

        if not _time:
            raise ValueError(
                f"Time string '{time_data}' does not match H:M or H:M:S format."
            )

    text = _format(_time.hour, _time.minute, _time.second, fmt, precision)

    return text


def thaiword_to_time(text: str, padding: bool = True) -> str:
    """
    Convert Thai time in words into time (H:M).

    :param str text: Thai time in words
    :param bool padding: Zero pad the hour if True

    :return: time string
    :rtype: str

    :Example:
    ::

        thaiword_to_time("บ่ายโมงครึ่ง")
        # output:
        # 13:30
    """
    keys_dict = list(_DICT_THAI_TIME.keys())
    text = text.replace("กว่า", "").replace("ๆ", "").replace(" ", "")
    _i = ["ตีหนึ่ง", "ตีสอง", "ตีสาม", "ตีสี่", "ตีห้า"]
    _time = ""
    for affix in _THAI_TIME_AFFIX:
        if affix in text and affix != "ตี":
            _time = text.replace(affix, affix + "|")
            break
        elif affix in text and affix == "ตี":
            for j in _i:
                if j in text:
                    _time = text.replace(j, j + "|")
                    break
        else:
            pass
    if "|" not in _time:
        raise ValueError("Cannot find any Thai word for time affix.")

    _LIST_THAI_TIME = _time.split("|")
    del _time

    hour = _THAI_TIME_CUT.word_tokenize(_LIST_THAI_TIME[0])
    minute = _LIST_THAI_TIME[1]
    if len(minute) > 1:
        minute = _THAI_TIME_CUT.word_tokenize(minute)
    else:
        minute = 0
    text = ""

    # determine hour
    if hour[-1] == "นาฬิกา" and hour[0] in keys_dict and hour[:-1]:
        text += str(thaiword_to_num("".join(hour[:-1])))
    elif hour[0] == "ตี" and hour[1] in keys_dict:
        text += str(_DICT_THAI_TIME[hour[1]])
    elif hour[-1] == "โมงเช้า" and hour[0] in keys_dict:
        if _DICT_THAI_TIME[hour[0]] < 6:
            text += str(_DICT_THAI_TIME[hour[0]] + 6)
        else:
            text += str(_DICT_THAI_TIME[hour[0]])
    elif (hour[-1] == "โมงเย็น" or hour[-1] == "โมง") and hour[0] == "บ่าย":
        text += str(_DICT_THAI_TIME[hour[1]] + 12)
    elif (hour[-1] == "โมงเย็น" or hour[-1] == "โมง") and hour[0] in keys_dict:
        text += str(_DICT_THAI_TIME[hour[0]] + 12)
    elif hour[-1] == "เที่ยงคืน":
        text += "0"
    elif hour[-1] == "เที่ยงวัน" or hour[-1] == "เที่ยง":
        text += "12"
    elif hour[0] == "บ่ายโมง":
        text += "13"
    elif hour[-1] == "ทุ่ม":
        if len(hour) == 1:
            text += "19"
        else:
            text += str(_DICT_THAI_TIME[hour[0]] + 18)

    if not text:
        raise ValueError("Cannot find any Thai word for hour.")

    if padding and len(text) == 1:
        text = "0" + text
    text += ":"

    # determine minute
    if minute:
        n = 0
        for affix in minute:
            if affix in keys_dict:
                if affix != "สิบ":
                    n += _DICT_THAI_TIME[affix]
                elif affix == "สิบ" and n != 0:
                    n *= 10
                elif affix == "สิบ" and n == 0:
                    n += 10
        if n != 0 and n > 9:
            text += str(n)
        else:
            text += "0" + str(n)
    else:
        text += "00"

    return text
