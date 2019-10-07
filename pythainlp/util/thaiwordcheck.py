# -*- coding: utf-8 -*-
"""
Check if it's an "authentic Thai word"
Adapted from
https://github.com/wannaphongcom/open-thai-nlp-document/blob/master/check_thai_word.md
"""
import re
import warnings

_THANTHAKHAT_CHAR = "\u0e4c"  # Thanthakhat (cancellation of sound)

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

_TH_PREFIX_DIPHTHONG = {"กะ", "กระ", "ปะ", "ประ"}  # คำควบกล้ำขึ้นตัน

_TH_CONSONANTS_PATTERN = re.compile(r"[ก-ฬฮ]", re.U)  # สำหรับตรวจสอบพยัญชนะ


def is_authentic_thai(word: str) -> bool:
    """
    Check if a word is an "authentic Thai word", in Thai it called "คำไทยแท้".

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

    English word::

        from pythainlp.util import is_authentic_thai

        is_authentic_thai("Avocado")
        # output: False

    Authentic Thai word::

        is_authentic_thai("มะม่วง")
        # output: True
        is_authentic_thai("ตะวัน")
        # output: True

    Non authentic Thai word:

        is_authentic_thai("สามารถ")
        # output: False
        is_authentic_thai("อิสริยาภรณ์")
        # output: False
    """
    # Exceptions
    if word in _TH_TRUE_THAI_WORD:
        return True

    # If a word contains Thanthakhat, it is not an authentic Thai
    if _THANTHAKHAT_CHAR in word:
        return False

    # If a word contains non-Thai char, it is not an authentic Thai
    for char in word:
        if char in _TH_NON_THAI_CHARS:
            return False

    res = re.findall(_TH_CONSONANTS_PATTERN, word)  # ดึงพยัญชนะทัั้งหมดออกมา
    if res == []:  # Do not contain any thai alphabets -> english word
        return False

    # If a word does not end with true final, it is not an authentic Thai
    if (len(res) == 1) or (res[len(res) - 1] in _TH_TRUE_FINALS):
        return True

    # Note: This will not work, as it check the whole word, not the prefix.
    # Prefix-sentitive tokenization is required in order to able to check this.
    if word in _TH_PREFIX_DIPHTHONG:
        return True
    return False


def thaicheck(word: str) -> bool:
    warnings.warn(
        "thaicheck is deprecated, use is_authentic_thai instead",
        DeprecationWarning
    )
    return is_authentic_thai(word)
