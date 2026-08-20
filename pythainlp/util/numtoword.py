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

__all__: list[str] = ["bahttext", "num_to_thaiword", "num_to_thaiword_float"]

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
_DIGITS: list[str] = [
    "ศูนย์",
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


def _num_to_thaiword_block(num: int) -> str:
    """Convert a positive integer < 1,000,000 to Thai text.

    This is the core logic for a single block of up to 6 digits.
    """
    if num == 0:
        return ""

    output = ""
    num_str = str(num)
    for place, value in enumerate(list(num_str[::-1])):
        if value != "0":
            output = _VALUES[int(value)] + _PLACES[place] + output

    for search, replac in _EXCEPTIONS.items():
        output = output.replace(search, replac)

    # เอ็ด rule: trailing หนึ่ง in ones place
    if num != 1 and output.endswith("หนึ่ง"):
        output = output[: -len("หนึ่ง")] + "เอ็ด"

    return output


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

    if number == 0:
        return "ศูนย์"

    number_abs = abs(number)
    number_str = str(number_abs)

    # Split into groups of 6 digits from right side
    groups: list[str] = []
    while number_str:
        group = number_str[-6:]
        number_str = number_str[:-6]
        groups.append(group)

    output = ""
    for i in range(len(groups) - 1, -1, -1):
        group_num = int(groups[i])
        if group_num > 0:
            output += _num_to_thaiword_block(group_num)
        if i > 0:
            output += "ล้าน"

    # Global เอ็ด rule: trailing หนึ่ง in the full text
    if number_abs != 1 and output.endswith("หนึ่ง"):
        output = output[: -len("หนึ่ง")] + "เอ็ด"

    if number < 0:
        output = "ลบ" + output

    return output


def num_to_thaiword_float(number: float) -> str:
    """Converts a floating-point number to Thai text.

    The integer part is converted using :func:`num_to_thaiword`.
    The decimal point is read as "จุด".
    Each digit after the decimal is read individually without place descriptions.

    :param float number: a floating-point number to be converted to Thai text
    :return: text representing the number in Thai
    :rtype: str
    :raises TypeError: if *number* is not a numeric type

    :Example:

        >>> from pythainlp.util import num_to_thaiword_float
        >>> num_to_thaiword_float(123.45)
        'หนึ่งร้อยยี่สิบสามจุดสี่ห้า'
        >>> num_to_thaiword_float(3.14159)
        'สามจุดหนึ่งสี่หนึ่งห้าเก้า'
    """
    if not isinstance(number, (int, float)):
        raise TypeError(
            f"number must be a numeric type, not {type(number).__name__!r}"
        )

    # Reject non-finite floats early (nan/inf), since they cannot be rendered.
    if isinstance(number, float):
        import math

        if not math.isfinite(number):
            raise ValueError("number must be a finite float")

    # Handle whole numbers (including integer types)
    if isinstance(number, int) or (isinstance(number, float) and number.is_integer()):
        return num_to_thaiword(int(number))

    # Capture sign for negative floats
    is_negative: bool = number < 0
    num_abs: float = abs(number)
    num_str: str = str(num_abs)

    # Handle scientific notation (e.g., "1e-05", "1.23e-10")
    if "e" in num_str or "E" in num_str:
        mantissa, exp_str = num_str.lower().split("e", 1)
        exponent: int = int(exp_str)

        if "." in mantissa:
            mant_int, mant_frac = mantissa.split(".", 1)
            digits = mant_int + mant_frac
            decimal_places = len(mant_frac)
        else:
            digits = mantissa
            decimal_places = 0

        shift = exponent - decimal_places
        if shift >= 0:
            num_str = digits + ("0" * shift)
        else:
            pos = len(digits) + shift
            if pos > 0:
                num_str = digits[:pos] + "." + digits[pos:]
            else:
                num_str = "0." + ("0" * (-pos)) + digits
    if "." not in num_str:
        result = num_to_thaiword(int(num_str))
    else:
        int_part, dec_part = num_str.split(".")
        result = num_to_thaiword(int(int_part))
        result += "จุด"
        for digit in dec_part:
            result += _DIGITS[int(digit)]

    if is_negative:
        result = "ลบ" + result

    return result
