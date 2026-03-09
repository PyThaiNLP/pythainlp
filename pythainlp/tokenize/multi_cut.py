# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Multi cut -- Thai word segmentation with maximum matching.
Original codes from Korakot Chaovavanich.

:See Also:
    * `Facebook post \
        <https://www.facebook.com/groups/408004796247683/permalink/431283740586455/>`_
    * `GitHub Gist \
        <https://gist.github.com/korakot/fe26c65dc9eed467f4497f784a805716>`_
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pythainlp.util import Trie

from pythainlp.tokenize import word_dict_trie


class LatticeString(str):
    """String that keeps possible tokenizations"""

    unique: bool
    multi: list[str]
    in_dict: bool

    def __new__(
        cls,
        value: str,
        multi: Optional[list[str]] = None,
        in_dict: bool = True,
    ) -> "LatticeString":
        return str.__new__(cls, value)

    def __init__(
        self,
        value: str,
        multi: Optional[list[str]] = None,
        in_dict: bool = True,
    ) -> None:
        self.unique: bool = True
        if multi:
            self.multi: list[str] = list(multi)
            if len(self.multi) > 1:
                self.unique = False
        else:
            self.multi = [value]
        self.in_dict: bool = in_dict  # if in dictionary


_RE_NONTHAI: str = r"""(?x)
[-a-zA-Z]+|       # Latin characters
\d+([,\.]\d+)*|   # numbers
[ \t]+|           # spaces
\r?\n             # newlines
"""
_PAT_NONTHAI: re.Pattern[str] = re.compile(_RE_NONTHAI)


def _multicut(
    text: str, custom_dict: Optional[Trie] = None
) -> Iterator[LatticeString]:
    """Return LatticeString"""
    if not custom_dict:
        custom_dict = word_dict_trie()
    len_text = len(text)
    words_at: defaultdict[int, list[str]] = defaultdict(
        list
    )  # main data structure

    def serialize(p: int, p2: int) -> Iterator[str]:  # helper function
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
            yield LatticeString(text[last_p:q0], list(serialize(last_p, q0)))
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


def mmcut(text: str) -> list[str]:
    res = []
    for w in _multicut(text):
        mm = min(w.multi, key=lambda x: x.count("/"))
        res.extend(mm.split("/"))
    return res


def _combine(ww: list[LatticeString]) -> Iterator[str]:
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


def segment(text: str, custom_dict: Optional[Trie] = None) -> list[str]:
    """Dictionary-based maximum matching word segmentation.

    :param text: text to be tokenized
    :type text: str
    :param custom_dict: tokenization dictionary,\
        defaults to a Trie generated from pythainlp.corpus.thai_words
    :type custom_dict: Trie, optional
    :return: list of segmented tokens
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = word_dict_trie()

    return list(_multicut(text, custom_dict=custom_dict))


def find_all_segment(
    text: str, custom_dict: Optional[Trie] = None
) -> list[str]:
    """Get all possible segment variations.

    :param text: input string to be tokenized
    :type text: str
    :param custom_dict: tokenization dictionary,\
        defaults to word_dict_trie()
    :type custom_dict: Trie, optional
    :return: list of segment variations
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = word_dict_trie()

    ww = list(_multicut(text, custom_dict=custom_dict))

    return list(_combine(ww))
