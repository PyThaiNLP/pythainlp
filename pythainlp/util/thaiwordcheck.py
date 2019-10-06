# -*- coding: utf-8 -*-
"""
From
https://github.com/wannaphongcom/open-thai-nlp-document/blob/master/check_thai_word.md
"""
import re

_TH_TRUE_FINALS = ["ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"]  # ตัวสะกดตรงตามาตรา
_TH_NON_THAI_CHARS = ['ฆ', 'ณ', 'ฌ', 'ฎ', 'ฏ', 'ฐ', 'ฑ',
                      'ฒ', 'ธ', 'ศ', 'ษ', 'ฬ']  # ตัวอักษรที่ไม่ใช่ไทยแท้
_TH_PREFIX_DIPHTHONG = ["กะ", "กระ", "ปะ", "ประ"]  # คำควบกล้ำขึ้นตัน
_KARAN_CHAR = "\u0e4c"  # ตัวการันต์


def _check1(word: str) -> bool:  # เช็คตัวสะกดว่าตรงตามมาตราไหม
    if word in _TH_TRUE_FINALS:
        return True
    return False


def _check2(word: str) -> bool:  # เช็คตัวการันต์ ถ้ามี ไม่ใช่คำไทยแท้
    if _KARAN_CHAR in word:
        return False
    return True


def _check3(word: str) -> bool:
    if word in _TH_NON_THAI_CHARS:  # ถ้ามี แสดงว่าไม่ใช่คำไทยแท้
        return False
    return True


def thaicheck(word: str) -> bool:
    """
    Check if a word is an "authentic Thai word", in Thai it called "คำไทยแท้".

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

    English word::

        from pythainlp.util import thaicheck

        thaicheck("Avocado")
        # output: False

    Authentic Thai word::

        thaicheck("มะม่วง")
        # output: True
        thaicheck("ตะวัน")
        # output: True

    Non authentic Thai word:

        thaicheck("สามารถ")
        # output: False
        thaicheck("อิสริยาภรณ์")
        # output: False
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

    if word in _TH_PREFIX_DIPHTHONG:
        return True

    return False
