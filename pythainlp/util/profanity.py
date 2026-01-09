# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Profanity detection for Thai language
"""
from typing import List, Union

from pythainlp.corpus.common import thai_profanity_words
from pythainlp.tokenize import word_tokenize


def contains_profanity(text: str, engine: str = "newmm") -> bool:
    """
    Check if the given text contains profanity words.

    :param str text: Thai text to check
    :param str engine: tokenization engine (default: "newmm")
    :return: True if text contains profanity, False otherwise
    :rtype: bool

    :Example:
    ::

        from pythainlp.util import contains_profanity

        print(contains_profanity("สวัสดีครับ"))
        # output: False

        print(contains_profanity("คำหยาบคาย"))
        # output: True if the word is in the profanity list
    """
    if not text:
        return False
    
    profanity_set = thai_profanity_words()
    tokens = word_tokenize(text, engine=engine)
    
    for token in tokens:
        if token in profanity_set:
            return True
    
    return False


def find_profanity(text: str, engine: str = "newmm") -> List[str]:
    """
    Find all profanity words in the given text.

    :param str text: Thai text to check
    :param str engine: tokenization engine (default: "newmm")
    :return: List of profanity words found in the text
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util import find_profanity

        print(find_profanity("สวัสดีครับ"))
        # output: []

        print(find_profanity("text with profanity words"))
        # output: ['profanity_word1', 'profanity_word2']
    """
    if not text:
        return []
    
    profanity_set = thai_profanity_words()
    tokens = word_tokenize(text, engine=engine)
    
    found_profanity = []
    for token in tokens:
        if token in profanity_set:
            found_profanity.append(token)
    
    return found_profanity


def censor_profanity(text: str, replacement: str = "*", engine: str = "newmm") -> str:
    """
    Replace profanity words in the text with a replacement character.

    :param str text: Thai text to censor
    :param str replacement: character to replace profanity with (default: "*")
    :param str engine: tokenization engine (default: "newmm")
    :return: Text with profanity words censored
    :rtype: str

    :Example:
    ::

        from pythainlp.util import censor_profanity

        print(censor_profanity("สวัสดีครับ"))
        # output: สวัสดีครับ

        print(censor_profanity("text with profanity word"))
        # output: text with *** word
    """
    if not text:
        return text
    
    profanity_set = thai_profanity_words()
    tokens = word_tokenize(text, engine=engine, keep_whitespace=True)
    
    censored_tokens = []
    for token in tokens:
        if token in profanity_set:
            censored_tokens.append(replacement * len(token))
        else:
            censored_tokens.append(token)
    
    return "".join(censored_tokens)
