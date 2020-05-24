# -*- coding: utf-8 -*-

DEFAULT_ROMANIZE_ENGINE = "royin"
DEFAULT_TRANSLITERATE_ENGINE = "thaig2p"


def romanize(text: str, engine: str = DEFAULT_ROMANIZE_ENGINE) -> str:
    """
    This function renders Thai words in the Latin alphabet or "romanization",
    using the Royal Thai General System of Transcription (RTGS)
    [#rtgs_transcription]_. RTGS is the official system published
    by the Royal Institute of Thailand. (Thai: ถอดเสียงภาษาไทยเป็นอักษรละติน)

    :param str text: Thai text to be romanized
    :param str engine: 'royin' (default) or 'thai2rom'

    :return: A string of Thai words rendered in the Latin alphabet.
    :rtype: str

    :Options for engines:
        * *royin* - (default) based on the Royal Thai General System of
          Transcription issued by Royal Institute of Thailand.
        * *thai2rom* - a deep learning-based Thai romanization engine
          (require PyTorch).

    :Example:
    ::

        from pythainlp.transliterate import romanize

        romanize("สามารถ", engine="royin")
        # output: 'samant'

        romanize("สามารถ", engine="thai2rom")
        # output: 'samat'

        romanize("ภาพยนตร์", engine="royin")
        # output: 'phapn'

        romanize("ภาพยนตร์", engine="thai2rom")
        # output: 'phapphayon'
    """

    if not text or not isinstance(text, str):
        return ""

    if engine == "thai2rom":
        from .thai2rom import romanize
    else:  # use default engine "royin"
        from .royin import romanize

    return romanize(text)


def transliterate(
    text: str, engine: str = DEFAULT_TRANSLITERATE_ENGINE
) -> str:
    """
    This function transliterates Thai text.

    :param str text: Thai text to be transliterated
    :param str engine: 'icu', 'ipa' (default), or 'thaig2p'

    :return: A string of phonetic alphabets indicating
             how the input text should be pronounced.
    :rtype: str

    :Options for engines:
        * *icu* - International Components for Unicode (ICU)
        * *ipa* - International Phonetic Alphabet (IPA) by epitran
        * *thaig2p* - (default) Thai Grapheme to Phoneme by deep learning
          output is International Phonetic Alphabet (IPA)
          (require PyTorch)

    :Example:
    ::

        from pythainlp.transliterate import transliterate

        transliterate("สามารถ", engine="thaig2p")
        # output: 's aː ˩˩˦ . m aː t̚ ˥˩'

        transliterate("สามารถ", engine="ipa")
        # output: 'saːmaːrot'

        transliterate("สามารถ", engine="icu")
        # output: 's̄āmārt̄h'

        transliterate("ภาพยนตร์", engine="thaig2p")
        # output:'pʰ aː p̚ ˥˩ . pʰ a ˦˥ . j o n ˧'

        transliterate("ภาพยนตร์", engine="ipa")
        # output: 'pʰaːpjanot'

        transliterate("ภาพยนตร์", engine="icu")
        # output: 'p̣hāphyntr̒'
    """

    if not text or not isinstance(text, str):
        return ""

    if engine == "icu" or engine == "pyicu":
        from .pyicu import transliterate
    elif engine == "thaig2p":
        from .thaig2p import transliterate
    else:
        from .ipa import transliterate

    return transliterate(text)
