# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Phonetic similarity of Thai words, based on IPA sounds."""

from __future__ import annotations

from typing import cast

import panphon
import panphon.distance

from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import pronunciate, transliterate

_ft: panphon.FeatureTable = panphon.FeatureTable()
_dst: panphon.distance.Distance = panphon.distance.Distance()


def _clean_ipa(ipa: str) -> str:
    """
    Clean IPA text by removing tones and spaces between phonetic codes.

    :param str ipa: International Phonetic Alphabet (IPA) text
    :return: IPA text with tones removed
    :rtype: str
    """
    return (
        ipa.replace("˩˩˦", "")
        .replace("˥˩", "")
        .replace("˨˩", "")
        .replace("˦˥", "")
        .replace("˧", "")
        .replace(" .", ".")
        .replace(". ", ".")
        .strip()
    )


def word2audio(word: str) -> str:
    """
    Convert a word to IPA.

    :param str word: Thai word to be converted
    :return: IPA text with tones removed
    :rtype: str

    :Example:

        >>> from pythainlp.soundex.sound import word2audio
        >>> word2audio("น้ำ")  # doctest: +SKIP
        'n aː m .'
    """
    _word = word_tokenize(word)
    _phone = [pronunciate(w, engine="w2p") for w in _word]
    _ipa = [
        _clean_ipa(transliterate(phone, engine="thaig2p")) for phone in _phone
    ]
    return ".".join(_ipa)


def audio_vector(word: str) -> list[list[int]]:
    """
    Convert a word to a list of phonetic feature vectors.

    :param str word: Thai word to be converted
    :return: list of features from panphon
    :rtype: list[list[int]]

    :Example:

        >>> from pythainlp.soundex.sound import audio_vector
        >>> audio_vector("น้ำ")  # doctest: +SKIP
        [[-1, 1, 1, -1, -1, -1, ...]]
    """
    return cast(
        "list[list[int]]",
        _ft.word_to_vector_list(word2audio(word), numeric=True),
    )


def word_approximation(word: str, list_word: list[str]) -> list[float]:
    """
    Calculate the phonetic distance from a word to each word in a list.

    :param str word: Thai word to be compared
    :param list[str] list_word: list of Thai words to compare against
    :return: list of distances to the words, in order
        (the smaller the value, the closer)
    :rtype: list[float]

    :Example:

        >>> from pythainlp.soundex.sound import word_approximation
        >>> word_approximation(
        ...     "รถ", ["รด", "รส", "รม", "น้ำ"]
        ... )  # doctest: +SKIP
        [0.0, 0.0, 3.875, 8.375]
    """
    _word = word2audio(word)
    _list_word = [word2audio(w) for w in list_word]
    _distance = [
        _dst.weighted_feature_edit_distance(_word, w) for w in _list_word
    ]
    return _distance
