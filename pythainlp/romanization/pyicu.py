# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import sys

try:
    import icu
except ImportError:
    from pythainlp.tools import install_package

    install_package("pyicu")
    try:
        import icu
    except ImportError:
        sys.exit("Error: please pip install pyicu")


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(data):
    """ถอดเสียงภาษาไทยเป็นอักษรละติน รับค่า ''str'' ข้อความ คืนค่า ''str'' อักษรละติน"""
    thai2latin = icu.Transliterator.createInstance("Thai-Latin")
    return thai2latin.transliterate(data)
