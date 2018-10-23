# -*- coding: utf-8 -*-
"""
Thai soundex

Credit: Korakot Chaovavanich
https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
"""
import re


def LK82(text):
    """
    LK82 - It's a thai soundex rule.

    :param str text: Thai word
    :return: LK82 soundex
    """
    t1 = str.maketrans(
        "กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ",
        "กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ",
    )
    t2 = str.maketrans(
        "กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ",
        "1111112333333333333333333444444445555555667777889AAABCDEEF",
    )
    res = []
    text = re.sub("[่-๋]", "", text)  # 4.ลบวรรณยุกต์
    text = re.sub("จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์", "", text)  # 4.ลบตัวการันต์
    text = re.sub("[็ํฺๆฯ]", "", text)  # 5.ทิ้งไม้ไต่คู่ ฯลฯ

    # 6.เข้ารหัสตัวแรก
    if "ก" <= text[0] <= "ฮ":
        res.append(text[0].translate(t1))
        text = text[1:]
    else:
        res.append(text[1].translate(t1))
        res.append(text[0].translate(t2))
        text = text[2:]

    # เข้ารหัสตัวที่เหลือ
    i_v = None  # ตำแหน่งตัวคั่นล่าสุด (สระ)
    for i, c in enumerate(text):
        if c in "ะัิี":  # 7. ตัวคั่นเฉยๆ
            i_v = i
            res.append("")
        elif c in "าๅึืู":  # 8.คั่นและใส่
            i_v = i
            res.append(c.translate(t2))
        elif c == "ุ":  # 9.สระอุ
            i_v = i
            if i == 0 or (text[i - 1] not in "ตธ"):
                res.append(c.translate(t2))
            else:
                res.append("")
        elif c in "หอ":
            if i + 1 < len(text) and (text[i + 1] in "ึืุู"):
                res.append(c.translate(t2))
        elif c in "รวยฤฦ":
            if i_v == i - 1 or (i + 1 < len(text) and (text[i + 1] in "ึืุู")):
                res.append(c.translate(t2))
        else:
            res.append(c.translate(t2))  # 12.

    # 13. เอาตัวซ้ำออก
    res2 = [res[0]]
    for i in range(1, len(res)):
        if res[i] != res[i - 1]:
            res2.append(res[i])

    # 14. เติมศูนย์ให้ครบ ถ้าเกินก็ตัด
    return ("".join(res2) + "0000")[:5]


def Udom83(text):
    """
    Udom83 - It's a Thai soundex rule.

    :param str text: Thai word
    :return: Udom83 soundex
    """
    tu1 = str.maketrans(
        "กขฃคฅฆงจฉชฌซศษสฎดฏตฐฑฒถทธณนบปผพภฝฟมญยรลฬฤฦวอหฮ",
        "กขขขขขงจชชชสสสสดดตตททททททนนบปพพพฟฟมยยรรรรรวอฮฮ",
    )
    tu2 = str.maketrans(
        "มวำกขฃคฅฆงยญณนฎฏดตศษสบปพภผฝฟหอฮจฉชซฌฐฑฒถทธรฤลฦ",
        "0001111112233344444445555666666777778888889999",
    )
    text = re.sub("รร([เ-ไ])", "ัน\\1", text)
    text = re.sub("รร([ก-ฮ][ก-ฮเ-ไ])", "ั\\1", text)
    text = re.sub("รร([ก-ฮ][ะ-ู่-์])", "ัน\\1", text)
    text = re.sub("รร", "ัน", text)
    text = re.sub("ไ([ก-ฮ]ย)", "\\1", text)
    text = re.sub("[ไใ]([ก-ฮ])", "\\1ย", text)
    text = re.sub("ำ(ม[ะ-ู])", "ม\\1", text)
    text = re.sub("ำม", "ม", text)
    text = re.sub("ำ", "ม", text)
    text = re.sub("จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์", "", text)
    text = re.sub("[ะ-์]", "", text)
    sd = text[0].translate(tu1)
    sd += text[1:].translate(tu2)

    return (sd + "000000")[:7]


if __name__ == "__main__":
    texts = ["รถ", "รส", "รด", "จัน", "จันทร์", "มัก", "มัค", "มรรค"]
    for text in texts:
        print("{} - LK82:{} Udom83:{}".format(text, LK82(text), Udom83(text)))
