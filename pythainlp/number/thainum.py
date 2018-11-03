# -*- coding: utf-8 -*-
"""
Convert Thai numbers

Adapted from
http://justmindthought.blogspot.com/2012/12/code-php.html
"""
import ast
import math

__all__ = ["bahttext", "num_to_thaiword"]

p = [
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
thaitonum = dict((x[2], x[1]) for x in p[1:])
p1 = dict((x[0], x[1]) for x in p[1:])
d1 = 0


# เลขไทยสู่เลข
def thai_num_to_num(text):
    """
    :param str text: Thai number characters such as '๑', '๒', '๓'
    :return: universal numbers such as '1', '2', '3'
    """
    thaitonum = dict((x[2], x[1]) for x in p[1:])
    return thaitonum[text]


def thai_num_to_text(text):
    """
    :param str text: Thai number characters such as '๑', '๒', '๓'
    :return: Thai numbers, spelled out in Thai
    """
    thaitonum = dict((x[2], x[0]) for x in p[1:])
    return thaitonum[text]


def num_to_thai_num(text):
    """
    :param text: universal numbers such as '1', '2', '3'
    :return: Thai number characters such as '๑', '๒', '๓'
    """
    thaitonum = dict((x[1], x[2]) for x in p[1:])
    return thaitonum[text]


def num_to_text(text):
    """
    :param text: universal numbers such as '1', '2', '3'
    :return: Thai numbers, spelled out in Thai
    """
    thaitonum = dict((x[1], x[0]) for x in p[1:])
    return thaitonum[text]


def text_to_num(text):
    """
    :param text: Thai numbers, spelled out in Thai
    :return: universal numbers such as '1', '2', '3'
    """
    thaitonum = dict((x[0], x[1]) for x in p[1:])
    return thaitonum[text]


def text_to_thai_num(text):
    """
    :param text: Thai numbers, spelled out in Thai
    :return: Thai numbers such as '๑', '๒', '๓'
    """
    thaitonum = dict((x[0], x[2]) for x in p[1:])
    return thaitonum[text]


def number_format(num, places=0):
    return "{:20,.2f}".format(num)


def bahttext(amount_number):
    """
    Converts a number to Thai text and adds a suffix of "Baht" currency.

    Similar to BAHTTEXT funcation in Excel
    """
    amount_number = number_format(amount_number, 2).replace(" ", "")
    pt = amount_number.find(".")
    number, fraction = "", ""
    amount_number1 = amount_number.split(".")

    if not pt:
        number = amount_number
    else:
        amount_number = amount_number.split(".")
        number = amount_number[0]
        fraction = int(amount_number1[1])

    ret = ""
    number = ast.literal_eval(number.replace(",", ""))
    baht = num_to_thaiword(number)
    if baht != "":
        ret = "".join([ret, baht, "บาท"])
    satang = num_to_thaiword(fraction)
    if satang != "":
        ret = "".join([ret, satang, "สตางค์"])
    else:
        ret = "".join([ret, "ถ้วน"])

    return ret


def num_to_thaiword(number):
    """
    :param float number: a float number (with decimals) indicating a quantity
    :return: a text that indicates the full amount in word form, properly ending each digit with the right term.
    """
    position_call = ["แสน", "หมื่น", "พัน", "ร้อย", "สิบ", ""]
    number_call = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]

    ret = ""
    if number == 0:
        return ret
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
            ret += number_call[d]
        if d:
            ret += position_call[pos]
        else:
            ret += ""
        number = number % divider
        divider = divider / 10
        pos += 1

    return ret


if __name__ == "__main__":
    print(bahtext(4000.0))
