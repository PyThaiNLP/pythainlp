# -*- coding: utf-8 -*-
"""
Longest-matching Thai word segmentation

Based on code from
https://github.com/patorn/thaitokenizer/blob/master/thaitokenizer/tokenizer.py
"""
import re

from pythainlp.tokenize import DEFAULT_DICT_TRIE

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
_TONAL_CHAR = ["่", "้", "๊", "๋"]
_ENDING_CHAR = ["ๆ", "ฯ"]

_RE_NONTHAI = re.compile(r"[A-Za-z\d]*")

_KNOWN = True
_UNKNOWN = False


class LongestMatchTokenizer(object):
    def __init__(self, trie):
        self.__trie = trie

    def __search_nonthai(self, text: str):
        match = _RE_NONTHAI.search(text)
        if match.group(0):
            return match.group(0).lower()
        return None

    def __is_next_word_valid(self, text: str, begin_pos: int) -> bool:
        len_text = len(text)
        text = text[begin_pos:len_text].strip()

        if not text:
            return True

        match = self.__search_nonthai(text)
        if match:
            return True

        for pos in range(len_text):
            if text[0:pos] in self.__trie:
                return True

        return False

    def __longest_matching(self, text: str, begin_pos: int):
        len_text = len(text)
        text = text[begin_pos:len_text]

        match = self.__search_nonthai(text)
        if match:
            return match

        word = None
        word_valid = None

        for pos in range(len_text):
            if text[0:pos] in self.__trie:
                word = text[0:pos]
                if self.__is_next_word_valid(text, pos):
                    word_valid = text[0:pos]

        if word:
            if not word_valid:
                word_valid = word

            try:
                if text[len(word_valid)] in _ENDING_CHAR:
                    return text[0 : (len(word_valid) + 1)]
                else:
                    return word_valid
            except BaseException:
                return word_valid
        else:
            return ""

    def __segment_text(self, text: str):
        if not text:
            return []

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
                        or text[begin_pos] in _TONAL_CHAR
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

        return tokens

    def tokenize(self, text):
        tokens = self.__segment_text(text)
        return tokens


def segment(text, trie=None):
    """ตัดคำภาษาไทยด้วยวิธี longest matching"""
    if not trie:
        trie = DEFAULT_DICT_TRIE

    return LongestMatchTokenizer(trie).tokenize(text)
