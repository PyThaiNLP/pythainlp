# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrap tltk, a Thai language toolkit."""

from __future__ import annotations

from pythainlp.transliterate._tltk_g2p import (
    tltk_syl_segment_native,
    tltk_word_segment_native,
)


def segment(text: str) -> list[str]:
    """
    Tokenize text into words with tltk.

    :param str text: text to be tokenized
    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []
    text = text.replace(" ", "<u/>")
    _temp: str = tltk_word_segment_native(text).replace("<u/>", " ").replace("<s/>", "")
    _temp_list = _temp.split("|")
    if _temp_list[-1] == "":
        del _temp_list[-1]
    return _temp_list


def syllable_tokenize(text: str) -> list[str]:
    """
    Tokenize text into syllables with tltk.

    :param str text: text to be tokenized
    :return: list of syllables
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []
    _temp: str = tltk_syl_segment_native(text)
    _temp_list = _temp.split("~")
    if _temp_list[-1] == "<s/>":
        del _temp_list[-1]
    return _temp_list


def sent_tokenize(text: str) -> list[str]:
    """
    Tokenize text into sentences with tltk.

    :param str text: text to be tokenized
    :return: list of sentences
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []
    text = text.replace(" ", "<u/>")
    _temp: str = tltk_word_segment_native(text).replace("<u/>", " ").replace("|", "")
    _temp_list = _temp.split("<s/>")
    if _temp_list[-1] == "":
        del _temp_list[-1]
    return _temp_list
