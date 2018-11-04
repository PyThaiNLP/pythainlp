# -*- coding: utf-8 -*-
"""
Convert Thai numbers

Adapted from
http://justmindthought.blogspot.com/2012/12/code-php.html
"""
import math

__all__ = ["bahttext", "num_to_thaiword"]

_p = [
    ["ภาษาไทย", "ตัวเลข", "เลขไทย"],
    ["หนึ่ง", "1", "๑"],
    ["สอง", "2", "๒"],
    ["สาม", "3", "๓"],
    ["สี่", "4", "๔"],
    ["ห้า", "5", "๕"],
    ["หก", "6", "๖"],
    ["หก", "7", "๗"],
    ["แปด", "8", "๘"],
    ["เก้า", "9", "๙"],
]


# เลขไทยสู่เลขอารบิก
def thai_num_to_num(text):
    """
    :param str text: Thai number characters such as '๑', '๒', '๓'
    :return: universal numbers such as '1', '2', '3'
    """
    thaitonum = dict((x[2], x[1]) for x in _p[1:])
    return thaitonum[text]


def thai_num_to_text(text):
    """
    :param str text: Thai number characters such as '๑', '๒', '๓'
    :return: Thai numbers, spelled out in Thai
    """
    thaitonum = dict((x[2], x[0]) for x in _p[1:])
    return thaitonum[text]


def num_to_thai_num(text):
    """
    :param text: universal numbers such as '1', '2', '3'
    :return: Thai number characters such as '๑', '๒', '๓'
    """
    thaitonum = dict((x[1], x[2]) for x in _p[1:])
    return thaitonum[text]


def num_to_text(text):
    """
    :param text: universal numbers such as '1', '2', '3'
    :return: Thai numbers, spelled out in Thai
    """
    thaitonum = dict((x[1], x[0]) for x in _p[1:])
    return thaitonum[text]


def text_to_num(text):
    """
    :param text: Thai numbers, spelled out in Thai
    :return: universal numbers such as '1', '2', '3'
    """
    thaitonum = dict((x[0], x[1]) for x in _p[1:])
    return thaitonum[text]


def text_to_thai_num(text):
    """
    :param text: Thai numbers, spelled out in Thai
    :return: Thai numbers such as '๑', '๒', '๓'
    """
    thaitonum = dict((x[0], x[2]) for x in _p[1:])
    return thaitonum[text]


def bahttext(number):
    """
    Converts a number to Thai text and adds a suffix of "Baht" currency.
    Precision will be fixed at two decimal places (0.00) to fits "Satang" unit.

    Similar to BAHTTEXT function in Excel
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


def num_to_thaiword(number):
    """
    :param float number: a float number (with decimals) indicating a quantity
    :return: a text that indicates the full amount in word form, properly ending each digit with the right term.
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


if __name__ == "__main__":
    print(bahttext(4000.0))
