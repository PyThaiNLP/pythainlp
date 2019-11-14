# -*- coding: utf-8 -*-
"""
thai_time() - Spell out time to Thai words
"""
from datetime import datetime, time
from typing import Union

from pythainlp.util.numtoword import num_to_thaiword

_TIME_FORMAT_WITH_SEC = "%H:%M:%S"
_TIME_FORMAT_WITHOUT_SEC = "%H:%M"


def _format_6h(h: int) -> str:
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

    return text


def _format_24h(h: int) -> str:
    """
    Thai time (24-hour clock)
    """
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
        raise NotImplementedError(fmt)

    if precision == "m" or precision == "s":
        if (
            m == 30
            and (s == 0 or precision == "m")
            and (fmt == "6h" or fmt == "m6h")
        ):
            text += "ครึ่ง"
        else:
            text += num_to_thaiword(m) + "นาที"
            if precision == "s":
                text += num_to_thaiword(s) + "วินาที"
    else:
        if m:
            if m == 30 and s == 0 and (fmt == "6h" or fmt == "m6h"):
                text += "ครึ่ง"
            else:
                text += num_to_thaiword(m) + "นาที"
        if s:
            text += num_to_thaiword(s) + "วินาที"

    return text


def thai_time(
    time_data: Union[time, datetime, str],
    fmt: str = "24h",
    precision: Union[str, None] = None,
) -> str:
    """
    Spell out time to Thai words.

    :param str time_data: time input, can be a datetime.time object \
        or a datetime.datetime object \
        or a string (in H:M or H:M:S format, using 24-hour clock)
    :param str fmt: time output format
        * *24h* - 24-hour clock (default)
        * *6h* - 6-hour clock
        * *m6h* - Modified 6-hour clock
    :param str precision: precision of the spell out
        * *m* - always spell out to minute level
        * *s* - always spell out to second level
        * None - spell out only non-zero parts
    :return: Time spell out in Thai words
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

        thai_time("18:30", fmt="m6h")
        # output:
        # หกโมงครึ่ง

        thai_time(datetime.time(12, 3, 0))
        # output:
        # สิบสองนาฬิกาสามนาที

        thai_time(datetime.time(12, 3, 0), precision="s")
        # output:
        # สิบสองนาฬิกาสามนาทีศูนย์วินาที
    """
    _time = None

    if isinstance(time_data, time) or isinstance(time_data, datetime):
        _time = time_data
    else:
        if not isinstance(time_data, str):
            raise TypeError(
                "Time data must be a datetime.time object, a datetime.datetime object, or a string."
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
