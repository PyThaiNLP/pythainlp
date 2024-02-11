# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Multi cut -- Thai word segmentation with maximum matching.
Original codes from Korakot Chaovavanich.

:See Also:
    * `Facebook post \
        <https://www.facebook.com/groups/408004796247683/permalink/431283740586455/>`_
    * `GitHub Gist \
        <https://gist.github.com/korakot/fe26c65dc9eed467f4497f784a805716>`_
"""

import re
from collections import defaultdict
from typing import Iterator, List

from pythainlp.tokenize import DEFAULT_WORD_DICT_TRIE
from pythainlp.util import Trie


class LatticeString(str):
    """String that keeps possible tokenizations"""

    def __new__(cls, value, multi=None, in_dict=True):
        return str.__new__(cls, value)

    def __init__(self, value, multi=None, in_dict=True):
        self.unique = True
        if multi:
            self.multi = list(multi)
            if len(self.multi) > 1:
                self.unique = False
        else:
            self.multi = [value]
        self.in_dict = in_dict  # if in dictionary


_RE_NONTHAI = r"""(?x)
[-a-zA-Z]+|       # Latin characters
\d+([,\.]\d+)*|   # numbers
[ \t]+|           # spaces
\r?\n             # newlines
"""
_PAT_NONTHAI = re.compile(_RE_NONTHAI)


def _multicut(
    text: str, custom_dict: Trie = DEFAULT_WORD_DICT_TRIE
) -> Iterator[LatticeString]:
    """Return LatticeString"""
    if not custom_dict:
        custom_dict = DEFAULT_WORD_DICT_TRIE

    len_text = len(text)
    words_at = defaultdict(list)  # main data structure

    def serialize(p, p2):  # helper function
        for w in words_at[p]:
            p_ = p + len(w)
            if p_ == p2:
                yield w
            elif p_ < p2:
                for path in serialize(p_, p2):
                    yield w + "/" + path

    q = {0}
    last_p = 0  # last position for yield
    while min(q) < len_text:
        p = min(q)
        q -= {p}  # q.pop, but for set

        for w in custom_dict.prefixes(text[p:]):
            words_at[p].append(w)
            q.add(p + len(w))

        len_q = len(q)

        if len_q == 1:
            q0 = min(q)
            yield LatticeString(text[last_p:q0], serialize(last_p, q0))
            last_p = q0
        elif len_q == 0:  # len(q) == 0  means not found in dictionary
            m = _PAT_NONTHAI.match(text[p:])
            if m:  # non-Thai token
                i = p + m.span()[1]
            else:  # non-Thai token, find minimum skip
                for i in range(p, len_text):
                    ww = custom_dict.prefixes(text[i:])
                    m = _PAT_NONTHAI.match(text[i:])
                    if ww or m:
                        break
                else:
                    i = len_text
            w = text[p:i]
            words_at[p].append(w)
            yield LatticeString(w, in_dict=False)
            last_p = i
            q.add(i)


def mmcut(text: str) -> List[str]:
    res = []
    for w in _multicut(text):
        mm = min(w.multi, key=lambda x: x.count("/"))
        res.extend(mm.split("/"))
    return res


def _combine(ww: List[LatticeString]) -> Iterator[str]:
    if ww == []:
        yield ""
    else:
        w = ww[0]
        for tail in _combine(ww[1:]):
            if w.unique:
                yield w + "|" + tail
            else:
                for m in w.multi:
                    yield m.replace("/", "|") + "|" + tail


def segment(
    text: str, custom_dict: Trie = DEFAULT_WORD_DICT_TRIE
) -> List[str]:
    """Dictionary-based maximum matching word segmentation.

    :param text: text to be tokenized
    :type text: str
    :param custom_dict: tokenization dictionary,\
        defaults to DEFAULT_WORD_DICT_TRIE
    :type custom_dict: Trie, optional
    :return: list of segmented tokens
    :rtype: List[str]
    """
    if not text or not isinstance(text, str):
        return []

    return list(_multicut(text, custom_dict=custom_dict))


def find_all_segment(
    text: str, custom_dict: Trie = DEFAULT_WORD_DICT_TRIE
) -> List[str]:
    """Get all possible segment variations.

    :param text: input string to be tokenized
    :type text: str
    :param custom_dict: tokenization dictionary,\
        defaults to DEFAULT_WORD_DICT_TRIE
    :type custom_dict: Trie, optional
    :return: list of segment variations
    :rtype: List[str]
    """
    if not text or not isinstance(text, str):
        return []

    ww = list(_multicut(text, custom_dict=custom_dict))

    return list(_combine(ww))
