# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Transliterating text to International Phonetic Alphabet (IPA)
Using epitran

:See Also:
    * `GitHub \
        <https://github.com/dmort27/epitran>`_
"""

from __future__ import annotations

from typing import cast

import epitran

_EPI_THA: epitran.Epitran = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    return cast(str, _EPI_THA.transliterate(text))


def trans_list(text: str) -> list[str]:
    return cast(list[str], _EPI_THA.trans_list(text))


def xsampa_list(text: str) -> list[str]:
    return cast(list[str], _EPI_THA.xsampa_list(text))
