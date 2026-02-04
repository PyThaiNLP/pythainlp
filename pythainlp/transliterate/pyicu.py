# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Transliterating text to International Phonetic Alphabet (IPA)
Using International Components for Unicode (ICU)

:See Also:
    * `GitHub \
        <https://github.com/ovalhub/pyicu>`_
"""

from __future__ import annotations

from icu import Transliterator

_ICU_THAI_TO_LATIN: Transliterator = Transliterator.createInstance(
    "Thai-Latin"
)


def transliterate(text: str) -> str:
    """Use ICU (International Components for Unicode) for transliteration

    :param str text: Thai text to be transliterated
    :return: A string of International Phonetic Alphabets indicating how the text should be pronounced
    :rtype: str
    """
    return str(_ICU_THAI_TO_LATIN.transliterate(text))
