# -*- coding: utf-8 -*-


def romanize(text: str, engine: str = "royin") -> str:
    """
    Romanization of Thai text
    ถอดเสียงภาษาไทยเป็นอักษรละติน
    :param str text: Thai text to be romanized
    :param str engine: 'royin' (default) or 'thai2rom'. 'royin' uses Thai Royal Institute standard. 'thai2rom' is deep learning Thai romanization (require keras).
    :return: English (more or less) text that spells out how the Thai text should be pronounced.
    """

    if not isinstance(text, str) or not text:
        return ""

    if engine == "thai2rom":
        from .thai2rom import romanize
    else:  # use default engine "royin"
        from .royin import romanize

    return romanize(text)


def transliterate(text: str, engine: str = "ipa") -> str:
    """
    Transliteration of Thai text
    :param str text: Thai text to be transliterated
    :param str engine: 'ipa' (International Phonetic Alphabet; default) or 'icu'.
    :return: A string of Internaitonal Phonetic Alphabets indicating how the text should be pronounced.
    """

    if not isinstance(text, str) or not text:
        return ""

    if engine == "icu" or engine == "pyicu":
        from .pyicu import transliterate
    else:
        from .ipa import transliterate

    return transliterate(text)
