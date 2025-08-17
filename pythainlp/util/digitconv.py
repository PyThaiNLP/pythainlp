# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Convert digits
"""

_arabic_thai = {
    "0": "๐",
    "1": "๑",
    "2": "๒",
    "3": "๓",
    "4": "๔",
    "5": "๕",
    "6": "๖",
    "7": "๗",
    "8": "๘",
    "9": "๙",
}

_thai_arabic = {
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
}

_digit_spell = {
    "0": "ศูนย์",
    "1": "หนึ่ง",
    "2": "สอง",
    "3": "สาม",
    "4": "สี่",
    "5": "ห้า",
    "6": "หก",
    "7": "เจ็ด",
    "8": "แปด",
    "9": "เก้า",
}

_spell_digit = {
    "ศูนย์": "0",
    "หนึ่ง": "1",
    "สอง": "2",
    "สาม": "3",
    "สี่": "4",
    "ห้า": "5",
    "หก": "6",
    "เจ็ด": "7",
    "แปด": "8",
    "เก้า": "9",
}

_arabic_thai_translate_table = str.maketrans(_arabic_thai)
_thai_arabic_translate_table = str.maketrans(_thai_arabic)
_digit_spell_translate_table = str.maketrans(_digit_spell)


def thai_digit_to_arabic_digit(text: str) -> str:
    """
    This function converts Thai digits (i.e. ๑, ๓, ๑๐) to Arabic digits
    (i.e. 1, 3, 10).

    :param str text: Text with Thai digits such as '๑', '๒', '๓'
    :return: Text with Thai digits converted to Arabic digits
             such as '1', '2', '3'
    :rtype: str

    :Example:
    ::

        from pythainlp.util import thai_digit_to_arabic_digit

        text = 'เป็นจำนวน ๑๒๓,๔๐๐.๒๕ บาท'

        thai_digit_to_arabic_digit(text)
        # output: เป็นจำนวน 123,400.25 บาท
    """
    if not text or not isinstance(text, str):
        raise TypeError("The text must be str type.")

    return text.translate(_thai_arabic_translate_table)


def arabic_digit_to_thai_digit(text: str) -> str:
    """
    This function converts Arabic digits (i.e. 1, 3, 10) to Thai digits
    (i.e. ๑, ๓, ๑๐).

    :param str text: Text with Arabic digits such as '1', '2', '3'
    :return: Text with Arabic digits converted to Thai digits
             such as '๑', '๒', '๓'
    :rtype: str

    :Example:
    ::

        from pythainlp.util import arabic_digit_to_thai_digit

        text = 'เป็นจำนวน 123,400.25 บาท'

        arabic_digit_to_thai_digit(text)
        # output: เป็นจำนวน ๑๒๓,๔๐๐.๒๕ บาท
    """
    if not text or not isinstance(text, str):
        raise TypeError("The text must be str type.")

    # Convert Arabic to Thai numerals
    return text.translate(_arabic_thai_translate_table)


def digit_to_text(text: str) -> str:
    """
    :param str text: Text with digits such as '1', '2', '๓', '๔'
    :return: Text with digits spelled out in Thai
    """
    if not text or not isinstance(text, str):
        raise TypeError("The text must be str type.")

    # Convert Thai numerals to Arabic ones
    text = text.translate(_thai_arabic_translate_table)
    # Spell out Arabic numerals in Thai text
    text = text.translate(_digit_spell_translate_table)
    return text


def text_to_arabic_digit(text: str) -> str:
    """
    This function converts spelled out digits in Thai to Arabic digits.

    :param text: A digit spelled out in Thai
    :return: An Arabic digit such as '1', '2', '3' if the text is
             digit spelled out in Thai (ศูนย์, หนึ่ง, สอง, ..., เก้า).
             Otherwise, it returns an empty string.
    :rtype: str

    :Example:
    ::

        from pythainlp.util import text_to_arabic_digit

        text_to_arabic_digit("ศูนย์")
        # output: 0
        text_to_arabic_digit("หนึ่ง")
        # output: 1
        text_to_arabic_digit("แปด")
        # output: 8
        text_to_arabic_digit("เก้า")
        # output: 9

        # For text that is not digit spelled out in Thai
        text_to_arabic_digit("สิบ") == ""
        # output: True
        text_to_arabic_digit("เก้าร้อย") == ""
        # output: True
    """
    if not isinstance(text, str):
        raise TypeError("The text must be str type.")
    elif not text or text not in _spell_digit:
        return ""

    return _spell_digit[text]


def text_to_thai_digit(text: str) -> str:
    """
    This function converts spelled out digits in Thai to Thai digits.

    :param text: A digit spelled out in Thai
    :return: A Thai digit such as '๑', '๒', '๓' if the text is digit
             spelled out in Thai (ศูนย์, หนึ่ง, สอง, ..., เก้า).
             Otherwise, it returns an empty string.
    :rtype: str

    :Example:
    ::

        from pythainlp.util import text_to_thai_digit

        text_to_thai_digit("ศูนย์")
        # output: ๐
        text_to_thai_digit("หนึ่ง")
        # output: ๑
        text_to_thai_digit("แปด")
        # output: ๘
        text_to_thai_digit("เก้า")
        # output: ๙

        # For text that is not Thai digit spelled out
        text_to_thai_digit("สิบ") == ""
        # output: True
        text_to_thai_digit("เก้าร้อย") == ""
        # output: True
    """
    if not isinstance(text, str):
        raise TypeError("The text must be str type.")
    elif not text:
        return ""

    return arabic_digit_to_thai_digit(text_to_arabic_digit(text))
