# -*- coding: utf-8 -*-
"""
โปรแกรม ETCC ใน Python
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
19 มิ.ย. 2560

วิธีใช้งาน
etcc(คำ)
คืนค่า โดยมี / แบ่งกลุ่มคำ
"""

import re

from pythainlp import thai_consonants

_UV = ["็", "ี", "ื", "ิ"]
_UV1 = ["ั", "ี"]
_LV = ["ุ", "ู"]
_C = "[" + thai_consonants + "]"
_UV2 = "[" + "".join(["ั", "ื"]) + "]"


def etcc(text: str) -> str:
    """
    Enhanced Thai Character Cluster (ETCC)

    :param string text: word input

    :return: etcc
    """

    if not text:
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

    return re.sub("//", "/", text)
