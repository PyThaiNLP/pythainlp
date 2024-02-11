# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Transliterating text to International Phonetic Alphabet (IPA)
Using International Components for Unicode (ICU)

:See Also:
    * `GitHub \
        <https://github.com/ovalhub/pyicu>`_
"""
from icu import Transliterator

_ICU_THAI_TO_LATIN = Transliterator.createInstance("Thai-Latin")


def transliterate(text: str) -> str:
    """
    Use ICU (International Components for Unicode) for transliteration
    :param str text: Thai text to be transliterated.
    :return: A string of Internaitonal Phonetic Alphabets indicating how the text should be pronounced.
    """
    return _ICU_THAI_TO_LATIN.transliterate(text)
