# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Convert number in words to a computable number value

First version of the code adapted from Korakot Chaovavanich's notebook
https://colab.research.google.com/drive/148WNIeclf0kOU6QxKd6pcfwpSs8l-VKD#scrollTo=EuVDd0nNuI8Q
"""
import re
from typing import List

from pythainlp.tokenize import Tokenizer
from pythainlp.corpus import thai_words

_ptn_digits = r"(|หนึ่ง|เอ็ด|สอง|ยี่|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า)"
_ptn_six_figures = (
    rf"({_ptn_digits}แสน)?({_ptn_digits}หมื่น)?({_ptn_digits}พัน)?"
    rf"({_ptn_digits}ร้อย)?({_ptn_digits}สิบ)?{_ptn_digits}?"
)
_ptn_thai_numerals = rf"(ลบ)?({_ptn_six_figures}ล้าน)*{_ptn_six_figures}"
_re_thai_numerals = re.compile(_ptn_thai_numerals)

_digits = {
    # "ศูนย์" was excluded as a special case
    "หนึ่ง": 1,
    "เอ็ด": 1,
    "สอง": 2,
    "ยี่": 2,
    "สาม": 3,
    "สี่": 4,
    "ห้า": 5,
    "หก": 6,
    "เจ็ด": 7,
    "แปด": 8,
    "เก้า": 9,
}
_powers_of_10 = {
    "สิบ": 10,
    "ร้อย": 100,
    "พัน": 1000,
    "หมื่น": 10000,
    "แสน": 100000,
    # "ล้าน" was excluded as a special case
}
_valid_tokens = (
    set(_digits.keys()) | set(_powers_of_10.keys()) | {"ล้าน", "ลบ"}
)
_tokenizer = Tokenizer(custom_dict=_valid_tokens)


def _check_is_thainum(word: str):
    for j in list(_digits.keys()):
        if j in word:
            return (True, "num")
    for j in ["สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน", "จุด", "ลบ"]:
        if j in word:
            return (True, "unit")
    return (False, None)


_dict_words = [i for i in list(thai_words()) if not _check_is_thainum(i)[0]]
_dict_words += list(_digits.keys())
_dict_words += ["สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน", "จุด"]

_tokenizer_thaiwords = Tokenizer(_dict_words)


def thaiword_to_num(word: str) -> int:
    """
    Converts the spelled-out numerals in Thai scripts into an actual integer.

    :param str word: Spelled-out numerals in Thai scripts
    :return: Corresponding integer value of the input
    :rtype: int

    :Example:
    ::

        from pythainlp.util import thaiword_to_num

        thaiword_to_num("ศูนย์")
        # output: 0

        thaiword_to_num("สองล้านสามแสนหกร้อยสิบสอง")
        # output: 2300612

    """
    if not isinstance(word, str):
        raise TypeError(f"The input must be a string; given {word!r}")
    if not word:
        raise ValueError("The input string cannot be empty")
    if word == "ศูนย์":
        return 0
    if not _re_thai_numerals.fullmatch(word):
        raise ValueError("The input string is not a valid Thai numeral")

    tokens = _tokenizer.word_tokenize(word)
    accumulated = 0
    next_digit = 1

    is_minus = False
    if tokens[0] == "ลบ":
        is_minus = True
        tokens.pop(0)

    for token in tokens:
        if token in _digits:
            next_digit = _digits[token]
        elif token in _powers_of_10:
            # Absent digit assumed 1 before all powers of 10 (except million)
            accumulated += max(next_digit, 1) * _powers_of_10[token]
            next_digit = 0
        else:  # token == "ล้าน"
            # Absent digit assumed 0 before word million
            accumulated = (accumulated + next_digit) * 1000000
            next_digit = 0

    # Cleaning up trailing digit
    accumulated += next_digit

    if is_minus:
        accumulated = -accumulated

    return accumulated


def _decimal_unit(words: list) -> float:
    _num = 0.0
    for i, v in enumerate(words):
        _num += int(thaiword_to_num(v)) / (10 ** (i + 1))
    return _num


def words_to_num(words: list) -> float:
    """
    Thai Words to float

    :param str text: Thai words
    :return: float of words
    :rtype: float

    :Example:
    ::

        from pythainlp.util import words_to_num

        words_to_num(["ห้า", "สิบ", "จุด", "เก้า", "ห้า"])
        # output: 50.95

    """
    num = 0
    if "จุด" not in words:
        num = thaiword_to_num("".join(words))
    else:
        words_int = "".join(words[: words.index("จุด")])
        words_float = words[words.index("จุด") + 1 :]
        num = thaiword_to_num(words_int)
        if num <= -1:
            num -= _decimal_unit(words_float)
        else:
            num += _decimal_unit(words_float)

    return num


def text_to_num(text: str) -> List[str]:
    """
    Thai text to list of Thai words with floating point numbers

    :param str text: Thai text with the spelled-out numerals
    :return: list of Thai words with float values of the input
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util import text_to_num

        text_to_num("เก้าร้อยแปดสิบจุดเก้าห้าบาทนี่คือจำนวนทั้งหมด")
        # output: ['980.95', 'บาท', 'นี่', 'คือ', 'จำนวน', 'ทั้งหมด']

        text_to_num("สิบล้านสองหมื่นหนึ่งพันแปดร้อยแปดสิบเก้าบาท")
        # output: ['10021889', 'บาท']

    """
    _temp = _tokenizer_thaiwords.word_tokenize(text)
    thainum = []
    last_index = -1
    list_word_new = []
    for i, word in enumerate(_temp):
        if (
            _check_is_thainum(word)[0]
            and last_index + 1 == i
            and i + 1 == len(_temp)
        ):
            thainum.append(word)
            list_word_new.append(str(words_to_num(thainum)))
        elif _check_is_thainum(word)[0] and last_index + 1 == i:
            thainum.append(word)
            last_index = i
        elif _check_is_thainum(word)[0]:
            thainum.append(word)
            last_index = i
        elif (
            not _check_is_thainum(word)[0]
            and last_index + 1 == i
            and last_index != -1
        ):
            list_word_new.append(str(words_to_num(thainum)))
            thainum = []
            list_word_new.append(word)
        else:
            list_word_new.append(word)
            last_index = -1
    return list_word_new
