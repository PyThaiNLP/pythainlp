# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Convert number value to Thai read out

Adapted from
https://justmindthought.blogspot.com/2012/12/code-php.html
https://suksit.com/post/writing-bahttext-in-php/
"""

from __future__ import annotations

from typing import Optional

__all__: list[str] = ["bahttext", "num_to_thaiword"]

_VALUES: list[str] = [
    "",
    "หนึ่ง",
    "สอง",
    "สาม",
    "สี่",
    "ห้า",
    "หก",
    "เจ็ด",
    "แปด",
    "เก้า",
]
_PLACES: list[str] = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
_EXCEPTIONS: dict[str, str] = {"หนึ่งสิบ": "สิบ", "สองสิบ": "ยี่สิบ", "สิบหนึ่ง": "สิบเอ็ด"}


def bahttext(number: float) -> str:
    """Converts a number to Thai text and adds
    a suffix "บาท" (Baht).
    The precision will be fixed at two decimal places (0.00)
    to fit "สตางค์" (Satang) unit.
    This function works similarly to the ``BAHTTEXT`` function in Microsoft Excel.

    :param float number: number to be converted into Thai Baht currency format
    :return: text representing the amount of money in the format
             of Thai currency
    :rtype: str
    :raises TypeError: if *number* is not a numeric type

    :Example:

        >>> from pythainlp.util import bahttext
        >>> bahttext(1)
        'หนึ่งบาทถ้วน'
        >>> bahttext(21)
        'ยี่สิบเอ็ดบาทถ้วน'
        >>> bahttext(200)
        'สองร้อยบาทถ้วน'
    """
    if not isinstance(number, (int, float)):
        raise TypeError(
            f"number must be a numeric type, not {type(number).__name__!r}"
        )

    ret = ""

    if number == 0:
        ret = "ศูนย์บาทถ้วน"
    else:
        num_int_str, num_dec_str = f"{number:.2f}".split(".")
        num_int = int(num_int_str)
        num_dec = int(num_dec_str)

        baht = num_to_thaiword(num_int)
        if baht:
            ret = "".join([ret, baht, "บาท"])

        satang = num_to_thaiword(num_dec)
        if satang and satang != "ศูนย์":
            ret = "".join([ret, satang, "สตางค์"])
        else:
            ret = "".join([ret, "ถ้วน"])

    return ret


def num_to_thaiword(number: Optional[int]) -> str:
    """Converts a number to Thai text.

    :param int number: an integer number to be converted to Thai text
    :return: text representing the number in Thai
    :rtype: str

    :Example:

        >>> from pythainlp.util import num_to_thaiword
        >>> num_to_thaiword(1)
        'หนึ่ง'
        >>> num_to_thaiword(11)
        'สิบเอ็ด'
    """
    if number is None:
        return ""

    output = ""
    number_temp = number
    if number == 0:
        output = "ศูนย์"

    number_str = str(abs(number))
    for place, value in enumerate(list(number_str[::-1])):
        if place % 6 == 0 and place > 0:
            output = _PLACES[6] + output

        if value != "0":
            output = _VALUES[int(value)] + _PLACES[place % 6] + output

    for search, replac in _EXCEPTIONS.items():
        output = output.replace(search, replac)

    # เอ็ด rule: trailing หนึ่ง in ones place (after any place marker)
    if number != 1 and number != -1 and output.endswith("หนึ่ง"):
        output = output[: -len("หนึ่ง")] + "เอ็ด"

    if number_temp < 0:
        output = "ลบ" + output

    return output
