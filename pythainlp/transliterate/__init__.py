# -*- coding: utf-8 -*-

from pythainlp.tokenize import word_tokenize

from .ipa import IPA
from .thai2rom import ThaiTransliterator

__all__ = ["IPA", "romanize", "ThaiTransliterator"]


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(text, engine="royin"):
    """
    :param str data: Thai text to be romanized
    :param str engine: 'royin' (default), 'pyicu', or 'thai2rom'. 'royin' uses Thai Royal Institute standard. 'pyicu' uses Internaitonal Phonetic Alphabet. 'thai2rom' is deep learning Thai romanization.
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
