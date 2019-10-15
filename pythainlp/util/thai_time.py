# -*- coding: utf-8 -*-
"""
Thai Time
by Wannaphong Phatthiyaphaibun
"""
from .numtoword import num_to_thaiword


def _type_6hr(h: int, m: int) -> str:
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


def _type_m6hr(h: int, m: int) -> str:
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


def _type_24hr(h: int, m: int) -> str:
    """
    Thai time (24-hour clock)
    """
    text = num_to_thaiword(h) + "นาฬิกา"
    if m != 0:
        text += num_to_thaiword(m) + "นาที"
    return text


def thai_time(time: str, fmt: str = "24-hour") -> str:
    """
    Convert time to Thai words.

    :param str time: time (H:m)
    :param str fmt: Thai time type
        * *24-hour* - 24-hour clock (default)
        * *6-hour* - 6-hour clock
        * *modified-6-hour* - Modified 6-hour clock
    :return: Thai time
    :rtype: str

    :Example:

        thai_time("8:17")
        # output:
        # แปดนาฬิกาสิบเจ็ดนาที

        thai_time("8:17", fmt="6-hour")
        # output:
        # สองโมงเช้าสิบเจ็ดนาที

        thai_time("8:17", fmt="modified-6-hour")
        # output:
        # แปดโมงสิบเจ็ดนาที
    """
    if not isinstance(time, str):
        raise TypeError("Input should be a string.")

    if not time or or ":" not in time:
        raise ValueError("Input string should be in H:m format")

    temp = time.split(":")
    h = int(temp[0])
    m = int(temp[1])

    text = ""
    if fmt == "6-hour":
        text = _type_6hr(h, m)
    elif fmt == "modified-6-hour":
        text = _type_m6hr(h, m)
    elif fmt == "24-hour":
        text = _type_24hr(h, m)
    else:
        raise NotImplementedError(fmt)

    return text
