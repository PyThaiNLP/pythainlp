# -*- coding: utf-8 -*-


def romanize(text: str, engine: str = "royin") -> str:
    """
    This function renders Thai words in the Latin alphabet or "romanization",
    using the Royal Thai General System of Transcription (RTGS)
    [rtgs_transcription]_. RTGS is the official system published
    by the Royal Institute of Thailand. (Thai: ถอดเสียงภาษาไทยเป็นอักษรละติน)

    :param str text: Thai text to be romanized
    :param str engine: 'royin' (default) or 'thai2rom'.

    :return: A string of Thai words rendered in the Latin alphabet.
    :rtype: str

    :Options for engines:
        * *royin* - uses the Royal Thai General System of Transcription issued
          by Royal Institute of Thailand .
        * *thai2rom* is a Thai romanization engine based on a deep learning
          model (require PyTorch).

    :Example:
        >>> from pythainlp.transliterate import romanize
        >>>
        >>> romanize("สามารถ", engine="royin"), romanize("สามารถ", \\
            engine="thai2rom")
        ('samant', 'samat')
        >>>
        >>> romanize("ภาพยนตร์", engine="royin"), romanize("ภาพยนตร์", \\
            engine="thai2rom")
        ('phapn', 'phapphayon')
        >>>
        >>> romanize("ปัญญา", engine="royin"), romanize("ปัญญา", \\
            engine="thai2rom")
        ('panna', 'panya')
        >>>
        >>> romanize("มหาชน", engine="royin"), romanize("มหาชน", \\
            engine="thai2rom")
        ('matn', 'mahachon')
        >>>
        >>> romanize("พลอย", engine="royin"), romanize("พลอย", \\
            engine="thai2rom")
        ('phnoi', 'phloi')
        >>>
        >>> romanize("นก", engine="royin"), romanize("นก", \\
            engine="thai2rom")
        ('nok', 'nok')
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
    This function transliterates Thai text.

    :param str text: Thai text to be transliterated
    :param str engine: 'ipa' (International Phonetic Alphabet; default)
                       or 'icu'.

    :return: A string of Internaitonal Phonetic Alphabets indicating
             how the text should be pronounced.
    :rtype: str

    :Options for engines:
        * *ipa* - (default) International Phonetic Alphabet (IPA)
        * *icu* - International Components for Unicode (ICU)

    :Example:
        >>> from pythainlp.transliterate import transliterate
        >>>
        >>> transliterate("สามารถ", engine="ipa"), \\
            transliterate("สามารถ", engine="icu")
        ('saːmaːrot','s̄āmārt̄h')
        >>>
        >>> transliterate("ภาพยนตร์", engine="ipa"), \\
            transliterate("ภาพยนตร์", engine="icu")
        ('pʰaːpjanot','p̣hāphyntr̒')
        >>>
        >>> transliterate("ปัญญา", engine="ipa"), \\
            transliterate("ปัญญา", engine="icu")
        ('pajjaː','pạỵỵā')
        >>>
        >>> transliterate("มหาชน", engine="ipa"), \\
            transliterate("มหาชน", engine="icu")
        ('mahaːt͡ɕʰon','mh̄āchn')
        >>>
        >>> transliterate("พลอย", engine="ipa"), \\
            transliterate("พลอย", engine="icu")
        ('pʰlɔːj','phlxy')
        >>>
        >>> transliterate("นก", engine="ipa"), \\
            transliterate("นก", engine="icu")
        ('nok','nk')
    """

    if not text or not isinstance(text, str):
        return ""

    if engine == "icu" or engine == "pyicu":
        from .pyicu import transliterate
    else:
        from .ipa import transliterate

    return transliterate(text)
