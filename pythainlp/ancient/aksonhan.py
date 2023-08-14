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
from pythainlp.util import Trie
from pythainlp import thai_consonants,thai_tonemarks
from pythainlp.tokenize import Tokenizer
from pythainlp.corpus import thai_orst_words


_dict_aksonhan = {}
for i in list(thai_consonants):
    if i=="ร":
        continue
    for j in list(thai_tonemarks):
        _dict_aksonhan[i+j+i] = "ั"+j+i
        _dict_aksonhan[i+i+j+i] = i+"ั"+j+i
    _dict_aksonhan[i+i] = "ั"+i
_set_aksonhan = set(_dict_aksonhan.keys())
_trie = Trie(list(_dict_aksonhan.keys())+list(thai_consonants))
_tokenizer = Tokenizer(custom_dict=_trie,engine="mm")
_dict_thai = set(thai_orst_words())  # call Thai words


def aksonhan_to_current(word:str)->str:
    """
    AksonHan words convert to current Thai words

    AksonHan (อักษรหัน) is write down two consonants as the \
    spelling of the /a/ vowels. (สระ อะ).

    Today, รร is an aksonHan words that still used in Thai.

    :param str word: Thai word
    :return: Thai AksonHan convert to current Thai words
    :rtype: str

    :Example:
    ::

        from pythainlp.ancient import aksonhan_to_current

        print(aksonhan_to_current("จกก"))
        # output: จัก

        print(aksonhan_to_current("บงงคบบ"))
        # output: บังคับ

        print(aksonhan_to_current("สรรเพชญ")) # รร is still used.
        # output: สรรเพชญ
    """
    if len(word) < 3:
        return word
    elif word in _set_aksonhan:
        return _dict_aksonhan[word]
    elif word in _dict_thai: # word in Thai words
        return word
    _seg = _tokenizer.word_tokenize(word)
    _w = []
    for i in _seg:
        if i in _set_aksonhan:
            _w.append(_dict_aksonhan[i])
        else:
            _w.append(i)
    return ''.join(_w)
