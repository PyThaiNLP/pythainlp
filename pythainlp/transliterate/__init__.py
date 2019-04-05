# -*- coding: utf-8 -*-

from pythainlp.tokenize import word_tokenize


# ถอดเสียงภาษาไทยเป็นอักษรละติน
def romanize(text, engine="royin"):
    """
    :param str text: Thai text to be romanized
    :param str engine: 'royin' (default) or 'thai2rom'. 'royin' uses Thai Royal Institute standard. 'thai2rom' is deep learning Thai romanization (require keras).
    :return: English (more or less) text that spells out how the Thai text should read.
    """

    if isinstance(text,str)==False:
        return ""

    if engine == "thai2rom":
        from .thai2rom import romanize

        return romanize(text)
    else:  # use default engine "royin"
        from .royin import romanize

        try:
            words = word_tokenize(text)
            romanized_words = [romanize(word) for word in words]
        except:
            romanized_words =[romanize(text)]
        return "".join(romanized_words)


def transliterate(text, engine="ipa"):
    """
    :param str text: Thai text to be transliterated
    :param str engine: 'ipa' (default) or 'pyicu'.
    :return: A string of Internaitonal Phonetic Alphabets indicating how the text should read.
    """

    if not text:
        return ""

    if engine == "pyicu":
        from .pyicu import transliterate
    else:
        from .ipa import transliterate

    return transliterate(text)
