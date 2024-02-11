# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Transliterating text to International Phonetic Alphabet (IPA)
Using epitran

:See Also:
    * `GitHub \
        <https://github.com/dmort27/epitran>`_
"""
from typing import List

import epitran

_EPI_THA = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    return _EPI_THA.transliterate(text)


def trans_list(text: str) -> List[str]:
    return _EPI_THA.trans_list(text)


def xsampa_list(text: str) -> List[str]:
    return _EPI_THA.xsampa_list(text)
