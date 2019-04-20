# -*- coding: utf-8 -*-


def romanize(text: str, engine: str = "royin") -> str:
    """
    Rendering Thai words in the Latin alphabet or "romanization",
    using the Royal Thai General System of Transcription (RTGS),
    which is the official system published by the Royal Institute of Thailand.
    ถอดเสียงภาษาไทยเป็นอักษรละติน
    :param str text: Thai text to be romanized
    :param str engine: 'royin' (default) or 'thai2rom'. 'royin' uses the Royal Thai General System of Transcription issued by Royal Institute of Thailand. 'thai2rom' is deep learning Thai romanization (require keras).
    :return: A string of Thai words rendered in the Latin alphabet.
    """

    if not text or not isinstance(text, str):
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

    if not text or not isinstance(text, str):
        return ""

    if engine == "icu" or engine == "pyicu":
        from .pyicu import transliterate
    else:
        from .ipa import transliterate

    return transliterate(text)
