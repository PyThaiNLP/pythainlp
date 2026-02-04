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

import epitran

_EPI_THA: epitran.Epitran = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    return _EPI_THA.transliterate(text)  # type: ignore[no-any-return]


def trans_list(text: str) -> list[str]:
    return _EPI_THA.trans_list(text)  # type: ignore[no-any-return]


def xsampa_list(text: str) -> list[str]:
    return _EPI_THA.xsampa_list(text)  # type: ignore[no-any-return]
