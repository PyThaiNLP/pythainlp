# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from itertools import chain

from pythainlp import thai_consonants, thai_tonemarks
from pythainlp.corpus import thai_orst_words
from pythainlp.tokenize import Tokenizer
from pythainlp.util import Trie

_dict_aksonhan: dict[str, str] = {}
i: str
for i in list(thai_consonants):
    if i == "ร":
        continue
    j: str
    for j in list(thai_tonemarks):
        _dict_aksonhan[i + j + i] = "ั" + j + i
        _dict_aksonhan[i + i + j + i] = i + "ั" + j + i
    _dict_aksonhan[i + i] = "ั" + i
_set_aksonhan: set[str] = set(_dict_aksonhan.keys())
_trie: Trie = Trie(chain(_dict_aksonhan.keys(), thai_consonants))
_tokenizer: Tokenizer = Tokenizer(custom_dict=_trie, engine="mm")
_dict_thai: set[str] = set(thai_orst_words())  # call Thai words


def aksonhan_to_current(word: str) -> str:
    """Convert AksonHan words to current Thai words

    AksonHan (อักษรหัน) writes two consonants to spell
    the short /a/ vowel (สระ อะ).

    Today, รร is an aksonhan pattern still used in Thai.

    :param str word: Thai word
    :return: Thai AksonHan to be converted to current Thai word
    :rtype: str

    :Example:

        >>> from pythainlp.ancient import aksonhan_to_current
        >>> print(aksonhan_to_current("จกก"))
        จัก
        >>> print(aksonhan_to_current("บงงคบบ"))
        บังคับ
        >>> print(aksonhan_to_current("สรรเพชญ"))  # รร is still used.
        สรรเพชญ

    """
    if len(word) < 3:
        return word
    elif word in _set_aksonhan:
        return _dict_aksonhan[word]
    elif word in _dict_thai:  # word in Thai words
        return word

    _seg = _tokenizer.word_tokenize(word)
    _w = []
    for i in _seg:
        if i in _set_aksonhan:
            _w.append(_dict_aksonhan[i])
        else:
            _w.append(i)
    return "".join(_w)
