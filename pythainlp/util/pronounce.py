# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List

from pythainlp.corpus import thai_words
from pythainlp.tokenize import syllable_tokenize
from pythainlp.khavee import KhaveeVerifier


kv = KhaveeVerifier()
all_thai_words_dict = None


def rhyme(word: str) -> List[str]:
    """
    Find Thai rhyme

    :param str word: A Thai word
    :return: All list Thai rhyme words
    :rtype: List[str]

    :Example:
    ::
        from pythainlp.util import rhyme

        print(rhyme("จีบ"))
        # output: ['กลีบ', 'กีบ', 'ครีบ', ...]
    """
    global all_thai_words_dict
    list_sumpus = []
    if all_thai_words_dict == None:
        all_thai_words_dict = [
            i for i in list(thai_words()) if len(syllable_tokenize(i)) == 1
        ]
    for i in all_thai_words_dict:
        if kv.is_sumpus(word, i) and i != word:
            list_sumpus.append(i)
    return sorted(list_sumpus)
