# -*- coding: utf-8 -*-
"""
Transliterating text to International Phonetic Alphabet (IPA)
Using epitran
https://github.com/dmort27/epitran
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
