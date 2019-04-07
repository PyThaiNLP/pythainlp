# -*- coding: utf-8 -*-
from icu import Transliterator


_ICU_THAI_TO_LATIN = Transliterator.createInstance("Thai-Latin")


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def transliterate(text: str) -> str:
    """
    ถอดเสียงภาษาไทยเป็นอักษรละติน รับค่า ''str'' ข้อความ คืนค่า ''str'' อักษรละติน
    """
    return _ICU_THAI_TO_LATIN.transliterate(text)
