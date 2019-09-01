# -*- coding: utf-8 -*-
"""
Enhanced Thai Character Cluster (ETCC)
Python implementation by Wannaphong Phatthiyaphaibun (19 June 2017)

:See Also:

Inrut, Jeeragone, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and Para Limmaneepraserth.
"Thai word segmentation using combination of forward and backward longest matching techniques."
In International Symposium on Communications and Information Technology (ISCIT), pp. 37-40. 2001.
"""

import re

from pythainlp import thai_consonants

_UV = ["็", "ี", "ื", "ิ"]
_UV1 = ["ั", "ี"]
_LV = ["ุ", "ู"]
_C = "[" + thai_consonants + "]"
_UV2 = "[" + "".join(["ั", "ื"]) + "]"


def segment(text: str) -> str:
    """
    Enhanced Thai Character Cluster (ETCC)

    :param string text: word input

    :return: etcc
    """

    if not text or not isinstance(text, str):
        return ""

    if re.search(r"[เแ]" + _C + r"[" + "".join(_UV) + r"]" + r"\w", text):
        search = re.findall(r"[เแ]" + _C + r"[" + "".join(_UV) + r"]" + r"\w", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search(_C + r"[" + "".join(_UV1) + r"]" + _C + _C + r"ุ" + r"์", text):
        search = re.findall(
            _C + r"[" + "".join(_UV1) + r"]" + _C + _C + r"ุ" + r"์", text
        )
        for i in search:
            text = re.sub(i, "//" + i + "/", text)

    if re.search(_C + _UV2 + _C, text):
        search = re.findall(_C + _UV2 + _C, text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)
    re.sub("//", "/", text)

    if re.search("เ" + _C + "า" + "ะ", text):
        search = re.findall("เ" + _C + "า" + "ะ", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search("เ" + r"\w\w" + "า" + "ะ", text):
        search = re.findall("เ" + r"\w\w" + "า" + "ะ", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)
    text = re.sub("//", "/", text)

    if re.search(_C + "[" + "".join(_UV1) + "]" + _C + _C + "์", text):
        search = re.findall(_C + "[" + "".join(_UV1) + "]" + _C + _C + "์", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search("/" + _C + "".join(["ุ", "์"]) + "/", text):
        # แก้ไขในกรณี พัน/ธุ์
        search = re.findall("/" + _C + "".join(["ุ", "์"]) + "/", text)
        for i in search:
            ii = re.sub("/", "", i)
            text = re.sub(i, ii + "/", text)

    text = re.sub("//", "/", text)

    return text.split("/")
