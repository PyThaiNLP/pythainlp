# -*- coding: utf-8 -*-
"""
Check if it's an "authentic Thai word"
Adapted from
https://github.com/wannaphongcom/open-thai-nlp-document/blob/master/check_thai_word.md
"""
import re

_TH_TRUE_THAI_WORD = {
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
}  # คำไทยแท้
_TH_TRUE_FINALS = {"ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"}  # ตัวสะกดตรงตามาตรา
_TH_NON_THAI_CHARS = {
    "ฆ",
    "ณ",
    "ฌ",
    "ฎ",
    "ฏ",
    "ฐ",
    "ฑ",
    "ฒ",
    "ธ",
    "ศ",
    "ษ",
    "ฬ",
}  # ตัวอักษรที่ไม่ใช่ไทยแท้
_TH_PREFIX_DIPHTHONG = {"กะ", "กระ", "ปะ", "ประ"}  # คำควบกล้ำขึ้นตัน
_THANTHAKHAT_CHAR = "\u0e4c"  # Thanthakhat (cancellation of sound)

_TH_CONSONANTS_PATTERN = re.compile(r"[ก-ฬฮ]", re.U)  # สำหรับตรวจสอบพยัญชนะ


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
    if word in _TH_TRUE_THAI_WORD:  # ข้อยกเว้น คำเหล่านี้เป็นคำไทยแท้
        return True

    res = re.findall(_TH_CONSONANTS_PATTERN, word)  # ดึงพยัญชนะทัั้งหมดออกมา
    if res == []:
        return False

    # If a word does not end with true final, it is not an authentic Thai
    if (len(res) == 1) or (res[len(res) - 1] in _TH_TRUE_FINALS):
        # If a word contains Thanthakhat, it is not an authentic Thai
        if _THANTHAKHAT_CHAR in word:
            return False
        else:
            chs = list(word)
            i = 0
            while i < len(chs):
                # If a word contains non-Thai char, it is not an authentic Thai
                if chs[i] not in _TH_NON_THAI_CHARS:
                    return False
                i += 1

            return True

    if word in _TH_PREFIX_DIPHTHONG:
        return True

    return False
