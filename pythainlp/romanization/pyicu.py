# -*- coding: utf-8 -*-

import sys

try:
    import icu
except ImportError:
    from pythainlp.tools import install_package

    install_package("pyicu")
    try:
        import icu
    except ImportError:
        raise ImportError("ImportError: Try 'pip install pyicu'")


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(data):
    """ถอดเสียงภาษาไทยเป็นอักษรละติน รับค่า ''str'' ข้อความ คืนค่า ''str'' อักษรละติน"""
    thai2latin = icu.Transliterator.createInstance("Thai-Latin")
    return thai2latin.transliterate(data)
