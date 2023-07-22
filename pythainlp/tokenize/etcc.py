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
"""
Segmenting text to Enhanced Thai Character Cluster (ETCC)
Python implementation by Wannaphong Phatthiyaphaibun

This implementation relies on a dictionary of ETCC created from etcc.txt
in pythainlp/corpus.

Notebook:
https://colab.research.google.com/drive/1UTQgxxMRxOr9Jp1B1jcq1frBNvorhtBQ

:See Also:

Jeeragone Inrut, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and
Para Limmaneepraserth. "Thai word segmentation using combination of forward
and backward longest matching techniques." In International Symposium on
Communications and Information Technology (ISCIT), pp. 37-40. 2001.
"""
import re
from typing import List

from pythainlp import thai_follow_vowels
from pythainlp.corpus import get_corpus
from pythainlp.tokenize import Tokenizer

_cut_etcc = Tokenizer(get_corpus("etcc.txt"), engine="longest")
_PAT_ENDING_CHAR = f"[{thai_follow_vowels}ๆฯ]"
_RE_ENDING_CHAR = re.compile(_PAT_ENDING_CHAR)


def _cut_subword(tokens: List[str]) -> List[str]:
    len_tokens = len(tokens)
    i = 0
    while True:
        if i == len_tokens:
            break
        if _RE_ENDING_CHAR.search(tokens[i]) and i > 0 and len(tokens[i]) == 1:
            tokens[i - 1] += tokens[i]
            del tokens[i]
            len_tokens -= 1
        i += 1
    return tokens


def segment(text: str) -> List[str]:
    """
    Segmenting text into ETCCs.

    Enhanced Thai Character Cluster (ETCC) is a kind of subword unit.
    The concept was presented in Inrut, Jeeragone, Patiroop Yuanghirun,
    Sarayut Paludkong, Supot Nitsuwat, and Para Limmaneepraserth.
    "Thai word segmentation using combination of forward and backward
    longest matching techniques." In International Symposium on Communications
    and Information Technology (ISCIT), pp. 37-40. 2001.

    :param str text: text to be tokenized to character clusters
    :return: list of clusters, tokenized from the text
    :return: List[str]
    """

    if not text or not isinstance(text, str):
        return []

    return _cut_subword(_cut_etcc.word_tokenize(text))
