# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Dictionary-based longest-matching Thai word segmentation. Implementation is based
on the codes from Patorn Utenpattanun.

:See Also:
    * `GitHub Repository \
       <https://github.com/patorn/thaitokenizer/blob/master/thaitokenizer/tokenizer.py>`_

"""
import re
from typing import Dict, List, Union

from pythainlp import thai_tonemarks
from pythainlp.tokenize import DEFAULT_WORD_DICT_TRIE
from pythainlp.util import Trie

_FRONT_DEP_CHAR = [
    "ะ",
    "ั",
    "า ",
    "ำ",
    "ิ",
    "ี",
    "ึ",
    "ื",
    "ุ",
    "ู",
    "ๅ",
    "็",
    "์",
    "ํ",
]
_REAR_DEP_CHAR = ["ั", "ื", "เ", "แ", "โ", "ใ", "ไ", "ํ"]
_TRAILING_CHAR = ["ๆ", "ฯ"]

_RE_NONTHAI = re.compile(r"[A-Za-z\d]*")

_KNOWN = True
_UNKNOWN = False


class LongestMatchTokenizer:
    def __init__(self, trie: Trie):
        self.__trie = trie

    @staticmethod
    def __search_nonthai(text: str) -> Union[None, str]:
        match = _RE_NONTHAI.search(text)
        if match.group(0):
            return match.group(0).lower()
        return None

    def __is_next_word_valid(self, text: str, begin_pos: int) -> bool:
        text = text[begin_pos:].strip()

        if not text:
            return True

        match = self.__search_nonthai(text)
        if match:
            return True

        for pos in range(len(text) + 1):
            if text[0:pos] in self.__trie:
                return True

        return False

    def __longest_matching(self, text: str, begin_pos: int) -> str:
        text = text[begin_pos:]

        match = self.__search_nonthai(text)
        if match:
            return match

        word = None
        word_valid = None

        for pos in range(len(text) + 1):
            w = text[0:pos]
            if w in self.__trie:
                word = w
                if self.__is_next_word_valid(text, pos):
                    word_valid = w

        if word:
            if not word_valid:
                word_valid = word

            try:
                len_word_valid = len(word_valid)
                if text[len_word_valid] in _TRAILING_CHAR:
                    return text[0 : len_word_valid + 1]
                else:
                    return word_valid
            except BaseException:
                return word_valid
        else:
            return ""

    def __segment(self, text: str):
        begin_pos = 0
        len_text = len(text)
        tokens = []
        token_statuses = []
        while begin_pos < len_text:
            match = self.__longest_matching(text, begin_pos)
            if not match:
                if (
                    begin_pos != 0
                    and not text[begin_pos].isspace()
                    and (
                        text[begin_pos] in _FRONT_DEP_CHAR
                        or text[begin_pos - 1] in _REAR_DEP_CHAR
                        or text[begin_pos] in thai_tonemarks
                        or (token_statuses and token_statuses[-1] == _UNKNOWN)
                    )
                ):
                    tokens[-1] += text[begin_pos]
                    token_statuses[-1] = _UNKNOWN
                else:
                    tokens.append(text[begin_pos])
                    token_statuses.append(_UNKNOWN)
                begin_pos += 1
            else:
                if begin_pos != 0 and text[begin_pos - 1] in _REAR_DEP_CHAR:
                    tokens[-1] += match
                else:
                    tokens.append(match)
                    token_statuses.append(_KNOWN)
                begin_pos += len(match)

        # Group consecutive spaces into one token
        grouped_tokens = []
        for token in tokens:
            if token.isspace() and grouped_tokens and grouped_tokens[-1].isspace():
                grouped_tokens[-1] += token
            else:
                grouped_tokens.append(token)

        return grouped_tokens

    def tokenize(self, text: str) -> List[str]:
        tokens = self.__segment(text)
        return tokens


_tokenizers: Dict[int, LongestMatchTokenizer] = {}


def segment(text: str, custom_dict: Trie = DEFAULT_WORD_DICT_TRIE) -> List[str]:
    """
    Dictionary-based longest matching word segmentation.

    :param str text: text to be tokenized into words
    :param pythainlp.util.Trie custom_dict: dictionary for tokenization
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = DEFAULT_WORD_DICT_TRIE

    global _tokenizers
    custom_dict_ref_id = id(custom_dict)
    if custom_dict_ref_id not in _tokenizers:
        _tokenizers[custom_dict_ref_id] = LongestMatchTokenizer(custom_dict)

    return _tokenizers[custom_dict_ref_id].tokenize(text)
