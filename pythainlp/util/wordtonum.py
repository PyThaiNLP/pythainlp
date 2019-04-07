# -*- coding: utf-8 -*-
"""
Convert number in words to a computable number value

Adapted from Korakot Chaovavanich's notebook
https://colab.research.google.com/drive/148WNIeclf0kOU6QxKd6pcfwpSs8l-VKD#scrollTo=EuVDd0nNuI8Q
"""
import re
from typing import Iterable, List

from pythainlp.tokenize import Tokenizer

_THAIWORD_NUMS = set("ศูนย์ หนึ่ง เอ็ด สอง ยี่ สาม สี่ ห้า หก เจ็ด แปด เก้า".split())
_THAIWORD_UNITS = set("สิบ ร้อย พัน หมื่น แสน ล้าน".split())
_THAIWORD_NUMS_UNITS = _THAIWORD_NUMS | _THAIWORD_UNITS

_THAI_INT_MAP = {
    "ศูนย์": 0,
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
    "สิบ": 10,
    "ร้อย": 100,
    "พัน": 1000,
    "หมื่น": 10000,
    "แสน": 100000,
    "ล้าน": 1000000,
}
_NU_PAT = re.compile("(.+)?(สิบ|ร้อย|พัน|หมื่น|แสน|ล้าน)(.+)?")  # หกสิบ, ร้อยเอ็ด
# assuming that the units are separated already

_TOKENIZER = Tokenizer(custom_dict=_THAIWORD_NUMS_UNITS)


def _thaiword_to_num(tokens: List[str]) -> int:
    if not tokens:
        return None

    len_tokens = len(tokens)

    if len_tokens == 1:
        return _THAI_INT_MAP[tokens[0]]

    if len_tokens == 2:
        a, b = tokens
        if b in _THAIWORD_UNITS:
            return _THAI_INT_MAP[a] * _THAI_INT_MAP[b]
        else:
            return _THAI_INT_MAP[a] + _THAI_INT_MAP[b]

    # longer case we use recursive
    a, b = tokens[:2]
    if a in _THAIWORD_UNITS and b != "ล้าน":  # ร้อย แปด
        return _THAI_INT_MAP[a] + _thaiword_to_num(tokens[1:])

    # most common case, a is a num, b is a unit
    if b in _THAIWORD_UNITS:
        return _THAI_INT_MAP[a] * _THAI_INT_MAP[b] + _thaiword_to_num(tokens[2:])


def thaiword_to_num(word: str) -> int:
    """
    Converts a Thai number spellout word to actual number value

    :param str word: a Thai number spellout
    :return: number
    """
    if not word:
        return None

    tokens = []
    if isinstance(word, str):
        tokens = _TOKENIZER.word_tokenize(word)
    elif isinstance(word, Iterable):
        for w in word:
            tokens.extend(_TOKENIZER.word_tokenize(w))

    res = []
    for tok in tokens:
        if tok in _THAIWORD_NUMS_UNITS:
            res.append(tok)
        else:
            m = _NU_PAT.fullmatch(tok)
            if m:
                res.extend([t for t in m.groups() if t])  # ตัด None ทิ้ง
            else:
                pass  # should not be here

    return _thaiword_to_num(res)
