# -*- coding: utf-8 -*-
"""
Thai soundex - LK82 system

Python implementation: Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""
import re

_TRANS1 = str.maketrans(
    "กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ",
    "กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ",
)
_TRANS2 = str.maketrans(
    "กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ",
    "1111112333333333333333333444444445555555667777889AAABCDEEF",
)

_RE_1 = re.compile(r"[่-๋]")
_RE_2 = re.compile(r"จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์")
_RE_3 = re.compile(r"[็ํฺๆฯ]")


def lk82(text: str) -> str:
    """
    LK82 - It's a Thai soundex rule.

    :param str text: Thai word
    :return: LK82 soundex
    """
    if not text:
        return ""

    text = _RE_1.sub("", text)  # 4.ลบวรรณยุกต์
    text = _RE_2.sub("", text)  # 4.ลบตัวการันต์
    text = _RE_3.sub("", text)  # 5.ทิ้งไม้ไต่คู่ ฯลฯ

    if not text:
        return ""

    # 6.เข้ารหัสตัวแรก
    res = []
    if "ก" <= text[0] <= "ฮ":
        res.append(text[0].translate(_TRANS1))
        text = text[1:]
    else:
        if len(text) > 1:
            res.append(text[1].translate(_TRANS1))
        res.append(text[0].translate(_TRANS2))
        text = text[2:]

    # เข้ารหัสตัวที่เหลือ
    i_v = None  # ตำแหน่งตัวคั่นล่าสุด (สระ)
    for i, c in enumerate(text):
        if c in "ะัิี":  # 7. ตัวคั่นเฉยๆ
            i_v = i
            res.append("")
        elif c in "าๅึืู":  # 8.คั่นและใส่
            i_v = i
            res.append(c.translate(_TRANS2))
        elif c == "ุ":  # 9.สระอุ
            i_v = i
            if i == 0 or (text[i - 1] not in "ตธ"):
                res.append(c.translate(_TRANS2))
            else:
                res.append("")
        elif c in "หอ":
            if i + 1 < len(text) and (text[i + 1] in "ึืุู"):
                res.append(c.translate(_TRANS2))
        elif c in "รวยฤฦ":
            if i_v == i - 1 or (i + 1 < len(text) and (text[i + 1] in "ึืุู")):
                res.append(c.translate(_TRANS2))
        else:
            res.append(c.translate(_TRANS2))  # 12.

    # 13. เอาตัวซ้ำออก
    res2 = [res[0]]
    for i in range(1, len(res)):
        if res[i] != res[i - 1]:
            res2.append(res[i])

    # 14. เติมศูนย์ให้ครบ ถ้าเกินก็ตัด
    return ("".join(res2) + "0000")[:5]
