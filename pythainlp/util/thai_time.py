# -*- coding: utf-8 -*-
"""
Thai Time
by Wannaphong Phatthiyaphaibun
"""
from datetime import datetime, time
from typing import Union

from pythainlp.util.numtoword import num_to_thaiword

_TIME_FORMAT_WITH_SEC = "%H:%M:%S"
_TIME_FORMAT_WITHOUT_SEC = "%H:%M"


def _format_6h(h: int, m: int, s: int) -> str:
    """
    Thai time (6-hour clock)
    """
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
        text += "บ่าย" + num_to_thaiword(h - 12) + "โมง"
    elif h == 18:
        text += "หกโมงเย็น"
    else:
        text += num_to_thaiword(h - 18) + "ทุ่ม"

    if m == 30:
        text += "ครึ่ง"
    elif m != 0:
        text += num_to_thaiword(m) + "นาที"

    return text


def _format_m6h(h: int, m: int, s: int) -> str:
    """
    Thai time (modified 6-hour clock)
    """
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

    if m == 30:
        text += "ครึ่ง"  # +"นาที"
    elif m != 0:
        text += num_to_thaiword(m) + "นาที"

    return text


def _format_24h(h: int, m: int, s: int) -> str:
    """
    Thai time (24-hour clock)
    """
    text = num_to_thaiword(h) + "นาฬิกา"
    if m != 0:
        text += num_to_thaiword(m) + "นาที"
    return text


def thai_time(time_string: Union[time, datetime, str], fmt: str = "24h") -> str:
    """
    Convert time to Thai words.

    :param str time_string: time input, can be a datetime.time object \
        or a datetime.datetime object \
        or a string (in H:M or H:M:S format, using 24-hour clock)
    :param str fmt: time output format
        * *24h* - 24-hour clock (default)
        * *6h* - 6-hour clock
        * *m6h* - Modified 6-hour clock
    :return: Time in Thai words
    :rtype: str

    :Example:

        thai_time("8:17")
        # output:
        # แปดนาฬิกาสิบเจ็ดนาที

        thai_time("8:17", "6h")
        # output:
        # สองโมงเช้าสิบเจ็ดนาที

        thai_time("8:17", "m6h")
        # output:
        # แปดโมงสิบเจ็ดนาที

        thai_time(datetime.time(12, 3))
        # output:
        # สิบสองนาฬิกาสามนาที
    """
    _time = None

    if isinstance(time_string, time) or isinstance(time_string, datetime):
        _time = time_string
    else:
        if not isinstance(time_string, str):
            raise TypeError(
                "Input must be a datetime.time object, a datetime.datetime object, or a string."
            )

        if not time_string:
            raise ValueError("Input string cannot be empty.")

        try:
            _time = datetime.strptime(time_string, _TIME_FORMAT_WITH_SEC)
            if not _time:
                _time = datetime.strptime(
                    time_string, _TIME_FORMAT_WITHOUT_SEC
                )
        except ValueError:
            pass

        if not _time:
            raise ValueError(
                "Input string must be in either H:M or H:M:S format."
            )

    format_func = None
    if fmt == "6h":
        format_func = _format_6h
    elif fmt == "m6h":
        format_func = _format_m6h
    elif fmt == "24h":
        format_func = _format_24h
    else:
        raise NotImplementedError(fmt)

    return format_func(_time.hour, _time.minute, _time.second)
