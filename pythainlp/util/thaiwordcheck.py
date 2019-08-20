# -*- coding: utf-8 -*-
"""
From
https://github.com/wannaphongcom/open-thai-nlp-document/blob/master/check_thai_word.md
"""
import re


def _check1(word: str) -> bool:  # เช็คตัวสะกดว่าตรงตามมาตราไหม
    if word in ["ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"]:
        return True
    return False


def _check2(word: str) -> bool:  # เช็คตัวการันต์ ถ้ามี ไม่ใช่คำไทยแท้
    if "์" in word:
        return False
    return True


def _check3(word: str) -> bool:
    if word in list("ฆณฌฎฏฐฑฒธศษฬ"):  # ถ้ามี แสดงว่าไม่ใช่คำไทยแท้
        return False
    return True


def thaicheck(word: str) -> bool:
    """
    Check if a word is an "authentic Thai word", in Thai it called "คำไทยแท้".

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

        English word:

        >>> from pythainlp.util import thaicheck
        >>> thaicheck("Avocado")
        False

        Authentic Thai word:

        >>> from pythainlp.util import thaicheck
        >>>
        >>> thaicheck("มะม่วง")
        True
        >>> thaicheck("ตะวัน")
        True

        Non authentic Thai word:

        >>> from pythainlp.util import thaicheck
        >>>
        >>> thaicheck("สามารถ")
        False
        >>> thaicheck("อิสริยาภรณ์")
        False
    """
    pattern = re.compile(r"[ก-ฬฮ]", re.U)  # สำหรับตรวจสอบพยัญชนะ
    res = re.findall(pattern, word)  # ดึงพยัญชนะทัั้งหมดออกมา

    if res == []:
        return False

    if _check1(res[len(res) - 1]) or len(res) == 1:
        if _check2(word):
            word2 = list(word)
            i = 0
            thai = True
            if word in [
                "ฆ่า",
                "เฆี่ยน",
                "ศึก",
                "ศอก",
                "เศิก",
                "เศร้า",
                "ธ",
                "ณ",
                "ฯพณฯ",
                "ใหญ่",
                "หญ้า",
                "ควาย",
                "ความ",
                "กริ่งเกรง",
                "ผลิ",
            ]:  # ข้อยกเว้น คำเหล่านี้เป็นคำไทยแท้
                return True

            while i < len(word2) and thai:
                thai = _check3(word2[i])
                if not thai:
                    return False
                i += 1
            return True

        return False

    if word in ["กะ", "กระ", "ปะ", "ประ"]:
        return True

    return False
