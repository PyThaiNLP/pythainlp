# -*- coding: utf-8 -*-
from icu import Transliterator


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(data):
    """
    ถอดเสียงภาษาไทยเป็นอักษรละติน รับค่า ''str'' ข้อความ คืนค่า ''str'' อักษรละติน
    """
    thai2latin = Transliterator.createInstance("Thai-Latin")

    return thai2latin.transliterate(data)
