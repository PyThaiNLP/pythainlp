# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from pythainlp.transliterate import pronunciate, transliterate
from pythainlp.tokenize import word_tokenize

import panphon
import panphon.distance

_ft = panphon.FeatureTable()
_dst = panphon.distance.Distance()

def _clean_ipa(ipa: str) -> str:
    """
    Clean IPA by remove tone and remove space between phone

    :param str ipa: IPA text
    :return: IPA that remove tone from the text
    :rtype: str
    """
    return ipa.replace("˩˩˦","").replace("˥˩","").replace("˨˩","").replace("˦˥","").replace("˧","").replace("˧","").replace(" .",".").replace(". ",".").strip()

def word2audio(word: str) -> str:
    """
    Convert word to IPA

    :param str word: Thai word
    :return: IPA that remove tone from the text
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
    :return: List feature from panphon
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
    :return: List of approximation of word (The smaller the value, the closer)
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
