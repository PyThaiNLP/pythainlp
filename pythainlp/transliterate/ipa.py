# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Transliterate text to International Phonetic Alphabet (IPA) using epitran.

:See Also:
    * `GitHub <https://github.com/dmort27/epitran>`_
"""

from __future__ import annotations

from typing import cast

import epitran

_EPI_THA: epitran.Epitran = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    """
    Transliterate Thai text to International Phonetic Alphabet (IPA).

    :param str text: Thai text to be transliterated
    :return: IPA text
    :rtype: str
    """
    return cast("str", _EPI_THA.transliterate(text))


def trans_list(text: str) -> list[str]:
    """
    Transliterate Thai text to a list of IPA segments.

    :param str text: Thai text to be transliterated
    :return: list of IPA segments
    :rtype: list[str]
    """
    return cast("list[str]", _EPI_THA.trans_list(text))


def xsampa_list(text: str) -> list[str]:
    """
    Transliterate Thai text to a list of X-SAMPA segments.

    :param str text: Thai text to be transliterated
    :return: list of X-SAMPA segments
    :rtype: list[str]
    """
    return cast("list[str]", _EPI_THA.xsampa_list(text))
