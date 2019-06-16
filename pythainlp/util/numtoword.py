# -*- coding: utf-8 -*-
"""
Convert number value to Thai read out

Adapted from
http://justmindthought.blogspot.com/2012/12/code-php.html
"""
import math

__all__ = ["bahttext", "num_to_thaiword"]


def bahttext(number: float) -> str:
    """
    This function converts a number to Thai text and adds
    a suffix "บาท" (Baht).
    The precision will be fixed at two decimal places (0.00)
    to fits "สตางค์" (Satang) unit.
    This function works similar to `BAHTTEXT` function in MS Excel.

    :param float number: number to be converted into Thai Baht currency format
    :return: text representing the amount of money in the format
             of Thai currency
    :rtype: str
    :Example:

        >>> from pythainlp.util import bahttext
        >>>
        >>> bahttext(1)
        หนึ่งบาทถ้วน
        >>>
        >>> bahttext(21)
        ยี่สิบเอ็ดบาทถ้วน
        >>>
        >>> bahttext(200)
        สองร้อยบาทถ้วน
        >>>
        >>> bahttext(1299.25)
        หนึ่งพันสองร้อยเก้าสิบเก้าบาทยี่สิบห้าสตางค์
        >>>
        >>> bahttext(2147483647.091)
        สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ดบาทเก้าสตางค์
        >>>
        >>> bahttext(0.16)
        ศูนย์บาทสิบหกสตางค์
        >>>
        >>> bahttext(0)
        ศูนย์บาทถ้วน
    """
    ret = ""

    if number is None:
        pass
    elif number == 0:
        ret = "ศูนย์บาทถ้วน"
    else:
        num_int, num_dec = "{:.2f}".format(number).split(".")
        num_int = int(num_int)
        num_dec = int(num_dec)

        baht = num_to_thaiword(num_int)
        if baht:
            ret = "".join([ret, baht, "บาท"])

        satang = num_to_thaiword(num_dec)
        if satang and satang != "ศูนย์":
            ret = "".join([ret, satang, "สตางค์"])
        else:
            ret = "".join([ret, "ถ้วน"])

    return ret


def num_to_thaiword(number: int) -> str:
    """
    This function convert number to Thai text

    :param int number: an integer number to be converted to Thai text
    :return: text representing the number in Thai
    :rtype: str

    :Example:
        >>> from pythainlp.util import num_to_thaiword
        >>>
        >>> num_to_thaiword(1)
        หนึ่ง
        >>>
        >>> num_to_thaiword(11)
        สิบเอ็ด
        >>>
        >>> num_to_thaiword(21)
        ยี่สิบเอ็ด
        >>>
        >>> num_to_thaiword(200)
        สองร้อย
        >>>
        >>> num_to_thaiword(1299.25)
        หนึ่งพันสองร้อยเก้าสิบเก้า
        >>>
        >>> num_to_thaiword(2147483647)
        สองพันหนึ่งร้อยสี่สิบเจ็ดล้านสี่แสนแปดหมื่นสามพันหกร้อยสี่สิบเจ็ด
        >>>
        >>> num_to_thaiword(0)
        ศูนย์
    """
    ret = ""

    if number is None:
        pass
    elif number == 0:
        ret = "ศูนย์"
    else:
        _POS_CALL = ["แสน", "หมื่น", "พัน", "ร้อย", "สิบ", ""]
        _NUM_CALL = [
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

        if number > 1000000:
            ret += num_to_thaiword(int(number / 1000000)) + "ล้าน"
            number = int(math.fmod(number, 1000000))
        divider = 100000

        pos = 0
        while number > 0:
            d = int(number / divider)

            if (divider == 10) and (d == 2):
                ret += "ยี่"
            elif (divider == 10) and (d == 1):
                ret += ""
            elif (divider == 1) and (d == 1) and (ret != ""):
                ret += "เอ็ด"
            else:
                ret += _NUM_CALL[d]

            if d:
                ret += _POS_CALL[pos]
            else:
                ret += ""

            number = number % divider
            divider = divider / 10
            pos += 1

    return ret
