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

from pythainlp.corpus.alphabet import get_data as thai_alphas

_UV = ["็", "ี", "ื", "ิ"]
_UV1 = ["ั", "ี"]
_LV = ["ุ", "ู"]
c = "[" + "".join(thai_alphas()) + "]"
_UV2 = "[" + "".join(["ั", "ื"]) + "]"


def etcc(text):
    """
    Enhanced Thai Character Cluster (ETCC)
    คั่นด้วย /
    รับ str
    ส่งออก str
    """
    if re.search(r"[เแ]" + c + r"[" + "".join(_UV) + r"]" + r"\w", text):
        search = re.findall(r"[เแ]" + c + r"[" + "".join(_UV) + r"]" + r"\w", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search(c + r"[" + "".join(_UV1) + r"]" + c + c + r"ุ" + r"์", text):
        search = re.findall(c + r"[" + "".join(_UV1) + r"]" + c + c + r"ุ" + r"์", text)
        for i in search:
            text = re.sub(i, "//" + i + "/", text)

    if re.search(c + _UV2 + c, text):
        search = re.findall(c + _UV2 + c, text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)
    re.sub("//", "/", text)

    if re.search("เ" + c + "า" + "ะ", text):
        search = re.findall("เ" + c + "า" + "ะ", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search("เ" + r"\w\w" + "า" + "ะ", text):
        search = re.findall("เ" + r"\w\w" + "า" + "ะ", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)
    text = re.sub("//", "/", text)

    if re.search(c + "[" + "".join(_UV1) + "]" + c + c + "์", text):
        search = re.findall(c + "[" + "".join(_UV1) + "]" + c + c + "์", text)
        for i in search:
            text = re.sub(i, "/" + i + "/", text)

    if re.search("/" + c + "".join(["ุ", "์"]) + "/", text):
        """แก้ไขในกรณี พัน/ธุ์"""
        search = re.findall("/" + c + "".join(["ุ", "์"]) + "/", text)
        for i in search:
            ii = re.sub("/", "", i)
            text = re.sub(i, ii + "/", text)

    return re.sub("//", "/", text)
