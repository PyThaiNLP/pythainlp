# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Look up romanized Thai words in a predefined dictionary compiled by Wannaphong, 2022.

Wannaphong Phatthiyaphaibun. (2022).
wannaphong/thai-english-transliteration-dictionary: v1.4 (v1.4).
Zenodo. https://doi.org/10.5281/zenodo.6716672
"""

from typing import Callable, Optional
from pythainlp.corpus.th_en_translit import (
    TRANSLITERATE_DICT,
    TRANSLITERATE_EN,
    TRANSLITERATE_FOLLOW_RTSG,
)


_TRANSLITERATE_IDX = 0


def follow_rtgs(text: str) -> Optional[bool]:
    """
    Check if the `text` follows romanization defined by Royal Society of Thailand (RTGS).
    :param str text: Text to look up. Must be a self-contained word.
    :return: True if text follows the definition by RTGS, False otherwise.
            `None` means unverified or unknown word.
    :rtype: Optional[bool]
    """
    try:
        follow = TRANSLITERATE_DICT[text][TRANSLITERATE_FOLLOW_RTSG][
            _TRANSLITERATE_IDX
        ]
    except IndexError:
        return None
    else:
        return follow


def _romanize(text: str, fallback_func: Callable[[str], str]) -> str:
    """
    Romanize one word. Look up first, call `fallback_func` if not found.
    """
    try:
        # try to get 0-th idx of look up result, simply ignore other possible variations.
        # not found means no mapping.
        lookup = TRANSLITERATE_DICT[text][TRANSLITERATE_EN][_TRANSLITERATE_IDX]
    except IndexError:
        return fallback_func(text)
    except TypeError as e:
        raise TypeError(f"`fallback_engine` is not callable. {e}")
    else:
        return lookup


def romanize(text: str, fallback_func: Callable[[str], str]) -> str:
    """
    Render Thai words in Latin alphabet by looking up
    Thai-English transliteration dictionary.

    :param str text: Thai text to be romanized
    :param Callable[[str], str] fallback_func: Callable
    :return: A string of Thai words rendered in the Latin alphabet
    :rtype: str
    """
    # split by whitespace. word_tokenizer may break text into subwords.
    # e.g. กาแลกซี่ -> ["กา", "แลก", "ซี่"]
    words = text.strip().split()
    romanized_words = [_romanize(word, fallback_func) for word in words]

    return " ".join(romanized_words)
