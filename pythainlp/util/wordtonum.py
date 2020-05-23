# -*- coding: utf-8 -*-
"""
Convert number in words to a computable number value

First version of the code adapted from Korakot Chaovavanich's notebook
https://colab.research.google.com/drive/148WNIeclf0kOU6QxKd6pcfwpSs8l-VKD#scrollTo=EuVDd0nNuI8Q
"""
import re

from pythainlp.tokenize import Tokenizer

_ptn_digits = r"(|หนึ่ง|เอ็ด|สอง|ยี่|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า)"
_ptn_six_figures = (
    fr"({_ptn_digits}แสน)?({_ptn_digits}หมื่น)?({_ptn_digits}พัน)?"
    fr"({_ptn_digits}ร้อย)?({_ptn_digits}สิบ)?{_ptn_digits}?"
)
_ptn_thai_numerals = fr"(ลบ)?({_ptn_six_figures}ล้าน)*{_ptn_six_figures}"
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
