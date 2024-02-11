# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List
import panphon
import panphon.distance
from pythainlp.transliterate import pronunciate, transliterate
from pythainlp.tokenize import word_tokenize

_ft = panphon.FeatureTable()
_dst = panphon.distance.Distance()

def _clean_ipa(ipa: str) -> str:
    """
    Clean IPA by removing tones and space between phonetic codes

    :param str ipa: IPA text
    :return: IPA with tones removed from the text
    :rtype: str
    """
    return ipa.replace("˩˩˦","").replace("˥˩","").replace("˨˩","").replace("˦˥","").replace("˧","").replace("˧","").replace(" .",".").replace(". ",".").strip()

def word2audio(word: str) -> str:
    """
    Convert word to IPA

    :param str word: Thai word
    :return: IPA with tones removed from the text
    :rtype: str

    :Example:
    ::

        from pythainlp.soundex.sound import word2audio

        word2audio("น้ำ")
        # output : 'n aː m .'
    """
    _word = word_tokenize(word)
    _phone = [pronunciate(w, engine="w2p") for w in _word]
    _ipa = [_clean_ipa(transliterate(phone, engine="thaig2p")) for phone in _phone]
    return '.'.join(_ipa)

def audio_vector(word:str) -> List[List[int]]:
    """
    Convert audio to vector list

    :param str word: Thai word
    :return: List of features from panphon
    :rtype: List[List[int]]

    :Example:
    ::

        from pythainlp.soundex.sound import audio_vector

        audio_vector("น้ำ")
        # output : [[-1, 1, 1, -1, -1, -1, ...]]
    """
    return _ft.word_to_vector_list(word2audio(word), numeric=True)

def word_approximation(word:str, list_word:List[str]):
    """
    Thai Word Approximation

    :param str word: Thai word
    :param str list_word: Thai word
    :return: List of approximation of words (The smaller the value, the closer)
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.soundex.sound import word_approximation

        word_approximation("รถ", ["รด", "รส", "รม", "น้ำ"])
        # output : [0.0, 0.0, 3.875, 8.375]
    """
    _word = word2audio(word)
    _list_word = [word2audio(w) for w in list_word]
    _distance = [_dst.weighted_feature_edit_distance(_word, w) for w in _list_word]
    return _distance
