# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from pythainlp.tokenize import word_tokenize


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(text, engine="royin"):
    """
    :param str data: Thai text to be romanized
    :param str engine: choose between 'royin' , 'pyicu' and 'thai2rom'. 'royin' will romanize according to the standard of Thai Royal Institute. 'pyicu' will romanize according to the Internaitonal Phonetic Alphabet. 'thai2rom' is deep learning thai romanization.
    :return: English (more or less) text that spells out how the Thai text should read.
    """
    if engine == "pyicu":
        from .pyicu import romanize
    elif engine == "thai2rom":
        from .thai2rom import ThaiTransliterator

        thai2rom = ThaiTransliterator()
        return thai2rom.romanize(text)
    else:  # use default engine "royin"
        from .royin import romanize

    words = word_tokenize(text)
    romanized_words = [romanize(word) for word in words]

    return "".join(romanized_words)
