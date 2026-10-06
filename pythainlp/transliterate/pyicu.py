# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Transliterate text using International Components for Unicode (ICU).

:See Also:
    * `GitHub <https://github.com/ovalhub/pyicu>`_
"""

from __future__ import annotations

from icu import Transliterator

_ICU_THAI_TO_LATIN: Transliterator = Transliterator.createInstance(
    "Thai-Latin"
)


def transliterate(text: str) -> str:
    """
    Transliterate Thai text using ICU (International Components for Unicode).

    :param str text: Thai text to be transliterated
    :return: text transliterated into Latin script
    :rtype: str
    """
    return str(_ICU_THAI_TO_LATIN.transliterate(text))
