# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

DEFAULT_ROMANIZE_ENGINE = "royin"
DEFAULT_TRANSLITERATE_ENGINE = "thaig2p"
DEFAULT_PRONUNCIATE_ENGINE = "w2p"


def romanize(
    text: str,
    engine: str = DEFAULT_ROMANIZE_ENGINE,
    fallback_engine: str = DEFAULT_ROMANIZE_ENGINE,
) -> str:
    """
    This function renders Thai word in the Latin alphabet or "romanization",
    using the Royal Thai General System of Transcription (RTGS)
    [#rtgs_transcription]_. RTGS is the official system published
    by the Royal Institute of Thailand. (Thai: ถอดเสียงภาษาไทยเป็นอักษรละติน)

    :param str text: A Thai word to be romanized. \
        The input should not include whitespace because \
        the function is support subwords by spliting whitespace.
    :param str engine: One of 'royin' (default), 'thai2rom', 'thai2rom_onnx, 'tltk', and 'lookup'. See more in options for engine section.
    :param str fallback_engine: If engine equals 'lookup', use `fallback_engine` for words that are not in the transliteration dict.
                                No effect on other engines. Default to 'royin'.

    :return: A string of a Thai word rendered in the Latin alphabet.
    :rtype: str

    :Options for engines:
        * *royin* - (default) based on the Royal Thai General System of
          Transcription issued by Royal Institute of Thailand.
        * *thai2rom* - a deep learning-based Thai romanization engine
          (require PyTorch).
        * *thai2rom_onnx* - a deep learning-based Thai romanization engine with ONNX runtime
        * *tltk* - TLTK: Thai Language Toolkit
        * *lookup* - Look up on Thai-English Transliteration dictionary v1.4 compiled by Wannaphong.

    :Example:
    ::

        from pythainlp.transliterate import romanize

        romanize("สามารถ", engine="royin")
        # output: 'samant'

        romanize("สามารถ", engine="thai2rom")
        # output: 'samat'

        romanize("สามารถ", engine="tltk")
        # output: 'samat'

        romanize("ภาพยนตร์", engine="royin")
        # output: 'phapn'

        romanize("รส ดี", engine="royin") # subwords
        # output: 'rot di'

        romanize("ภาพยนตร์", engine="thai2rom")
        # output: 'phapphayon'

        romanize("ภาพยนตร์", engine="thai2rom_onnx")
        # output: 'phapphayon'

        romanize("ก็อปปี้", engine="lookup")
        # output: 'copy'

    """

    def select_romanize_engine(engine: str):
        if engine == "thai2rom":
            from pythainlp.transliterate.thai2rom import romanize
        elif engine == "thai2rom_onnx":
            from pythainlp.transliterate.thai2rom_onnx import romanize
        elif engine == "tltk":
            from pythainlp.transliterate.tltk import romanize
        else:  # use default engine "royin"
            from pythainlp.transliterate.royin import romanize

        return romanize

    if not text or not isinstance(text, str):
        return ""

    if engine == "lookup":
        from pythainlp.transliterate.lookup import romanize

        fallback = select_romanize_engine(fallback_engine)
        return romanize(text, fallback_func=fallback)
    else:
        rom_engine = select_romanize_engine(engine)
        trans_word = []
        for subword in text.split(' '):
            trans_word.append(rom_engine(subword))
        new_word = ' '.join(trans_word)
        return new_word


def transliterate(
    text: str, engine: str = DEFAULT_TRANSLITERATE_ENGINE
) -> str:
    """
    This function transliterates Thai text.

    :param str text: Thai text to be transliterated
    :param str engine: 'icu', 'ipa', or 'thaig2p' (default)

    :return: A string of phonetic alphabets indicating
             how the input text should be pronounced.
    :rtype: str

    :Options for engines:
        * *thaig2p* - (default) Thai Grapheme-to-Phoneme,
          output is IPA (require PyTorch)
        * *icu* - pyicu, based on International Components for Unicode (ICU)
        * *ipa* - epitran, output is International Phonetic Alphabet (IPA)
        * *tltk_g2p* - Thai Grapheme-to-Phoneme from\
            `TLTK <https://pypi.org/project/tltk/>`_.,
        * *iso_11940* - Thai text into Latin characters with ISO 11940.
        * *tltk_ipa* - tltk, output is International Phonetic Alphabet (IPA)
        * *thaig2p_v2* - Thai Grapheme-to-Phoneme,
          output is IPA. https://huggingface.co/pythainlp/thaig2p-v2.0
        * *umt5_thaig2p* - Thai Grapheme-to-Phoneme,
          output is IPA, powered by UMT5.\
          https://huggingface.co/B-K/umt5-thai-g2p-v2-0.5k

    :Example:
    ::

        from pythainlp.transliterate import transliterate

        transliterate("สามารถ", engine="icu")
        # output: 's̄āmārt̄h'

        transliterate("สามารถ", engine="ipa")
        # output: 'saːmaːrot'

        transliterate("สามารถ", engine="thaig2p")
        # output: 's aː ˩˩˦ . m aː t̚ ˥˩'

        transliterate("สามารถ", engine="tltk_ipa")
        # output: 'saː5.maːt3'

        transliterate("สามารถ", engine="tltk_g2p")
        # output: 'saa4~maat2'

        transliterate("สามารถ", engine="iso_11940")
        # output: 's̄āmārt̄h'

        transliterate("ภาพยนตร์", engine="icu")
        # output: 'p̣hāphyntr̒'

        transliterate("ภาพยนตร์", engine="ipa")
        # output: 'pʰaːpjanot'

        transliterate("ภาพยนตร์", engine="thaig2p")
        # output: 'pʰ aː p̚ ˥˩ . pʰ a ˦˥ . j o n ˧'

        transliterate("ภาพยนตร์", engine="iso_11940")
        # output: 'p̣hāphyntr'
    """

    if not text or not isinstance(text, str):
        return ""

    if engine in ("icu", "pyicu"):
        from pythainlp.transliterate.pyicu import transliterate
    elif engine == "ipa":
        from pythainlp.transliterate.ipa import transliterate
    elif engine == "tltk_g2p":
        from pythainlp.transliterate.tltk import tltk_g2p as transliterate
    elif engine == "tltk_ipa":
        from pythainlp.transliterate.tltk import tltk_ipa as transliterate
    elif engine == "iso_11940":
        from pythainlp.transliterate.iso_11940 import transliterate
    elif engine == "thaig2p_v2":
        from pythainlp.transliterate.thaig2p_v2 import transliterate
    elif engine == "umt5_thaig2p":
        from pythainlp.translate.umt5_thaig2p import transliterate
    else:  # use default engine: "thaig2p"
        from pythainlp.transliterate.thaig2p import transliterate

    return transliterate(text)


def pronunciate(word: str, engine: str = DEFAULT_PRONUNCIATE_ENGINE) -> str:
    """
    This function pronunciates Thai word.

    :param str word: Thai text to be pronunciated
    :param str engine: 'w2p' (default)

    :return: A string of Thai letters indicating
             how the input text should be pronounced.
    :rtype: str

    :Options for engines:
        * *w2p* - Thai Word-to-Phoneme

    :Example:
    ::

        from pythainlp.transliterate import pronunciate

        pronunciate("สามารถ", engine="w2p")
        # output: 'สา-มาด'

        pronunciate("ภาพยนตร์", engine="w2p")
        # output: 'พาบ-พะ-ยน'
    """
    if not word or not isinstance(word, str):
        return ""

    # if engine == "w2p":  # has only one engine
    from pythainlp.transliterate.w2p import pronunciate

    return pronunciate(word)
