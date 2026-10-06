# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Spell out time as Thai words.

Convert time string or time object to Thai words.
"""

from __future__ import annotations

from contextlib import suppress
from datetime import datetime, time
from functools import lru_cache
from typing import Callable, Optional, Union

from pythainlp.tokenize import Tokenizer
from pythainlp.util.numtoword import num_to_thaiword
from pythainlp.util.wordtonum import thaiword_to_num

_TIME_FORMAT_WITH_SEC: str = "%H:%M:%S"
_TIME_FORMAT_WITHOUT_SEC: str = "%H:%M"
_DICT_THAI_TIME: dict[str, int] = {
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


@lru_cache
def _thai_time_cut() -> Tokenizer:
    """Lazy load Thai time tokenizer with cache"""
    return Tokenizer(custom_dict=list(_DICT_THAI_TIME.keys()), engine="newmm")


_THAI_TIME_AFFIX: list[str] = [
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


# Hour formatters by output format name; looked up with ``==``
_HOUR_FORMATTERS: tuple[tuple[str, Callable[[int], str]], ...] = (
    ("6h", _format_6h),
    ("m6h", _format_m6h),
    ("24h", _format_24h),
)
_HALF_HOUR_FORMATS: tuple[str, str] = ("6h", "m6h")


def _format_with_precision(
    m: int, s: int, fmt: str, precision: Optional[str]
) -> str:
    """Spell out minutes and seconds when precision is "m" or "s"."""
    if m == 30 and (s == 0 or precision == "m") and fmt in _HALF_HOUR_FORMATS:
        return "ครึ่ง"
    text = num_to_thaiword(m) + "นาที"
    if precision == "s":
        text += num_to_thaiword(s) + "วินาที"
    return text


def _format_non_zero(m: int, s: int, fmt: str) -> str:
    """Spell out only the non-zero minutes and seconds."""
    text = ""
    if m:
        if m == 30 and s == 0 and fmt in _HALF_HOUR_FORMATS:
            text += "ครึ่ง"
        else:
            text += num_to_thaiword(m) + "นาที"
    if s:
        text += num_to_thaiword(s) + "วินาที"
    return text


def _format(
    h: int,
    m: int,
    s: int,
    fmt: str = "24h",
    precision: Optional[str] = None,
) -> str:
    for name, formatter in _HOUR_FORMATTERS:
        if fmt == name:
            text = formatter(h)
            break
    else:
        raise NotImplementedError(f"Time format not supported: {fmt}")

    if precision in ("m", "s"):
        return text + _format_with_precision(m, s, fmt, precision)
    return text + _format_non_zero(m, s, fmt)


def time_to_thaiword(
    time_data: Union[time, datetime, str],
    fmt: str = "24h",
    precision: Optional[str] = None,
) -> str:
    """Spell out time as Thai words.

    :param time_data: time input; a :class:`datetime.time` object,
        a :class:`datetime.datetime` object, or a string
        in ``H:M`` or ``H:M:S`` format (24-hour clock)
    :type time_data: datetime.time or datetime.datetime or str
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

        >>> from datetime import time
        >>> from pythainlp.util import time_to_thaiword
        >>> time_to_thaiword("8:17")
        'แปดนาฬิกาสิบเจ็ดนาที'
        >>> time_to_thaiword("8:17", "6h")
        'สองโมงเช้าสิบเจ็ดนาที'
        >>> time_to_thaiword("8:17", "m6h")
        'แปดโมงสิบเจ็ดนาที'
        >>> time_to_thaiword("18:30", fmt="m6h")
        'หกโมงครึ่ง'
        >>> time_to_thaiword(time(12, 3, 0))
        'สิบสองนาฬิกาสามนาที'
        >>> time_to_thaiword(time(12, 3, 0), precision="s")
        'สิบสองนาฬิกาสามนาทีศูนย์วินาที'
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
            with suppress(ValueError):
                _time = datetime.strptime(time_data, _TIME_FORMAT_WITHOUT_SEC)

        if not _time:
            raise ValueError(
                f"Time string '{time_data}' does not match H:M or H:M:S format."
            )

    text = _format(_time.hour, _time.minute, _time.second, fmt, precision)

    return text


_TI_HOURS: tuple[str, ...] = (
    "ตีหนึ่ง",
    "ตีสอง",
    "ตีสาม",
    "ตีสี่",
    "ตีห้า",
    "ตีหก",
)


def _mark_affix(text: str) -> str:
    """Insert "|" after the hour affix; return "" if none is found.

    Affixes are tried in order. A non-"ตี" affix ends the search;
    a "ตี" match does not, so a later affix can override it.
    """
    marked = ""
    for affix in _THAI_TIME_AFFIX:
        if affix not in text:
            continue
        if affix != "ตี":
            return text.replace(affix, affix + "|")
        for ti_hour in _TI_HOURS:
            if ti_hour in text:
                marked = text.replace(ti_hour, ti_hour + "|")
                break
    return marked


def _is_evening(last: str) -> bool:
    return last == "โมงเย็น" or last == "โมง"


def _hour_from_morning_six(hour: list[str]) -> str:
    value = _DICT_THAI_TIME[hour[0]]
    return str(value + 6 if value < 6 else value)


def _hour_from_thum(hour: list[str]) -> Optional[str]:
    """Convert hours ending in ทุ่ม; None if the first token is unknown."""
    if len(hour) == 1:
        return "19"
    if hour[0] not in _DICT_THAI_TIME:
        return None
    return str(_DICT_THAI_TIME[hour[0]] + 18)


def _hour_from_unit(hour: list[str]) -> Optional[str]:
    """Convert hours ending in นาฬิกา, ตี, โมง; None if no rule matches."""
    if hour[-1] == "นาฬิกา" and hour[0] in _DICT_THAI_TIME and hour[:-1]:
        return str(thaiword_to_num("".join(hour[:-1])))
    if hour[0] == "ตี" and hour[1] in _DICT_THAI_TIME:
        return str(_DICT_THAI_TIME[hour[1]])
    if hour[-1] == "โมงเช้า" and hour[0] in _DICT_THAI_TIME:
        return _hour_from_morning_six(hour)
    if _is_evening(hour[-1]) and hour[0] == "บ่าย":
        if hour[1] not in _DICT_THAI_TIME:
            return None
        return str(_DICT_THAI_TIME[hour[1]] + 12)
    if _is_evening(hour[-1]) and hour[0] in _DICT_THAI_TIME:
        return str(_DICT_THAI_TIME[hour[0]] + 12)
    return None


def _hour_from_name(hour: list[str]) -> Optional[str]:
    """Convert named hours (เที่ยง, บ่ายโมง, ทุ่ม); None if no rule matches."""
    if hour[-1] == "เที่ยงคืน":
        return "0"
    if hour[-1] == "เที่ยงวัน" or hour[-1] == "เที่ยง":
        return "12"
    if hour[0] == "บ่ายโมง":
        return "13"
    if hour[-1] == "ทุ่ม":
        return _hour_from_thum(hour)
    return None


def _hour_text(hour: list[str]) -> str:
    """Convert hour tokens to the hour number; "" if no rule matches.

    The first matching rule wins; an earlier rule shadows a later one.
    """
    text = _hour_from_unit(hour)
    if text is None:
        text = _hour_from_name(hour)
    return text if text is not None else ""


def _minute_text(minute: Union[list[str], int]) -> str:
    """Convert minute tokens to a two-digit (or longer) minute string."""
    if not (minute and isinstance(minute, list)):
        return "00"
    n = 0
    for affix in minute:
        if affix not in _DICT_THAI_TIME:
            continue
        if affix != "สิบ":
            n += _DICT_THAI_TIME[affix]
        elif n != 0:
            n *= 10
        else:
            n += 10
    if n > 9:
        return str(n)
    return "0" + str(n)


def thaiword_to_time(text: str, padding: bool = True) -> str:
    """Convert Thai time in words into time (H:M).

    :param str text: Thai time in words
    :param bool padding: Zero pad the hour if True

    :return: time string
    :rtype: str

    :Example:

        >>> from pythainlp.util import thaiword_to_time
        >>> thaiword_to_time("บ่ายโมงครึ่ง")
        '13:30'
    """
    text = text.replace("กว่า", "").replace("ๆ", "").replace(" ", "")
    marked = _mark_affix(text)
    if "|" not in marked:
        raise ValueError("Cannot find any Thai word for time affix.")

    hour_raw, minute_raw = marked.split("|")[:2]
    hour = _thai_time_cut().word_tokenize(hour_raw)
    minute: Union[list[str], int]
    if len(minute_raw) > 1:
        minute = _thai_time_cut().word_tokenize(minute_raw)
    else:
        minute = 0

    hour_text = _hour_text(hour)
    if not hour_text:
        raise ValueError("Cannot find any Thai word for hour.")

    if padding and len(hour_text) == 1:
        hour_text = "0" + hour_text

    return hour_text + ":" + _minute_text(minute)
