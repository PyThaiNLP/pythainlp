# -*- coding: utf-8 -*-
"""
Transliterating text to International Phonetic Alphabet (IPA)
"""
import epitran

_EPI_THA = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    return _EPI_THA.transliterate(text)


def trans_list(text):
    return _EPI_THA.trans_list(text)


def xsampa_list(text):
    return _EPI_THA.xsampa_list(text)
