# -*- coding: utf-8 -*-
"""
Utility functions
"""
import re

from nltk.util import ngrams
from pythainlp import thai_tonemarks


def is_thaichar(ch):  # เป็นอักษรไทยหรือไม่
    ch_val = ord(ch)
    if ch_val >= 3584 and ch_val <= 3711:
        return True
    return False


def is_thaiword(word):  # เป็นคำที่มีแต่อักษรไทยหรือไม่
    for ch in word:
        if ch != "." and not is_thaichar(ch):
            return False
    return True


def bigrams(sequence):
    """
    Return list of bigrams
    """
    return ngrams(sequence, 2)


def trigrams(sequence):
    """
    Return list of trigrams
    """
    return ngrams(sequence, 3)


_NORMALIZE_RULE1 = [
    "ะ",
    "ั",
    "็",
    "า",
    "ิ",
    "ี",
    "ึ",
    "่",
    "ํ",
    "ุ",
    "ู",
    "ใ",
    "ไ",
    "โ",
    "ื",
    "่",
    "้",
    "๋",
    "๊",
    "ึ",
    "์",
    "๋",
    "ำ",
]  # เก็บพวกสระ วรรณยุกต์ที่ซ้ำกันแล้วมีปัญหา


_NORMALIZE_RULE2 = [
    ("เเ", "แ"),  # เ เ -> แ
    ("ํ(t)า", "\\1ำ"),
    ("ํา(t)", "\\1ำ"),
    ("([่-๋])([ัิ-ื])", "\\2\\1"),
    ("([่-๋])([ูุ])", "\\2\\1"),
    ("ำ([่-๋])", "\\1ำ"),
    ("(์)([ัิ-ื])", "\\2\\1"),
]  # เก็บพวก พิมพ์ลำดับผิดหรือผิดแป้นแต่กลับแสดงผลถูกต้อง ให้ไปเป็นแป้นที่ถูกต้อง เช่น เ + เ ไปเป็น แ


def normalize(text):
    """
    จัดการกับข้อความภาษาไทยให้เป็นปกติ
    normalize(text)
    คืนค่า str
    ตัวอย่าง
    >>> print(normalize("เเปลก")=="แปลก") # เ เ ป ล ก กับ แปลก
    True
    """
    for data in _NORMALIZE_RULE2:
        text = re.sub(data[0].replace("t", "[่้๊๋]"), data[1], text)
    for data in list(zip(_NORMALIZE_RULE1, _NORMALIZE_RULE1)):
        text = re.sub(data[0].replace("t", "[่้๊๋]") + "+", data[1], text)
    return text


def deletetone(text):
    """
    Remove tonemarks
    """
    chars = [ch for ch in text if ch not in thai_tonemarks]
    return "".join(chars)


# Notebook : https://colab.research.google.com/drive/148WNIeclf0kOU6QxKd6pcfwpSs8l-VKD#scrollTo=EuVDd0nNuI8Q
# Cr. Korakot Chaovavanich
thaiword_nums = set("ศูนย์ หนึ่ง เอ็ด สอง ยี่ สาม สี่ ห้า หก เจ็ด แปด เก้า".split())
thaiword_units = set("สิบ ร้อย พัน หมื่น แสน ล้าน".split())
thaiword_nums_units = thaiword_nums | thaiword_units
thai_int_map = {
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
nu_pat = re.compile("(.+)?(สิบ|ร้อย|พัน|หมื่น|แสน|ล้าน)(.+)?")  # หกสิบ, ร้อยเอ็ด
# assuming that the units are separated already


def _listtext_num2num(tokens):
    len_tokens = len(tokens)

    if len_tokens == 0:
        return 0

    if len_tokens == 1:
        return thai_int_map[tokens[0]]

    if len_tokens == 2:
        a, b = tokens
        if b in thaiword_units:
            return thai_int_map[a] * thai_int_map[b]
        else:
            return thai_int_map[a] + thai_int_map[b]

    # longer case we use recursive
    a, b = tokens[:2]
    if a in thaiword_units and b != "ล้าน":  # ร้อย แปด
        return thai_int_map[a] + _listtext_num2num(tokens[1:])

    # most common case, a isa num, b isa unit
    if b in thaiword_units:
        return thai_int_map[a] * thai_int_map[b] + _listtext_num2num(tokens[2:])


def listtext_num2num(tokens):
    res = []
    for tok in tokens:
        if tok in thaiword_nums_units:
            res.append(tok)
        else:
            m = nu_pat.fullmatch(tok)
            if m:
                res.extend([t for t in m.groups() if t])  # ตัด None ทิ้ง
            else:
                pass  # should not be here
    return _listtext_num2num(res)
