# -*- coding: utf-8 -*-
"""
Segmenting text to Enhanced Thai Character Cluster (ETCC)
Python implementation by Wannaphong Phatthiyaphaibun

Notebook:
https://colab.research.google.com/drive/1UTQgxxMRxOr9Jp1B1jcq1frBNvorhtBQ

:See Also:

Inrut, Jeeragone, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and Para Limmaneepraserth.
"Thai word segmentation using combination of forward and backward longest matching techniques."
In International Symposium on Communications and Information Technology (ISCIT), pp. 37-40. 2001.
"""
import re
from typing import List

from pythainlp.corpus import get_corpus
from pythainlp.tokenize import Tokenizer

_cut_etcc = Tokenizer(get_corpus("etcc.txt"), engine="longest")
_PAT_ENDING_CHAR = "[ะาๆฯๅำ]"
_RE_ENDING_CHAR = re.compile(_PAT_ENDING_CHAR)


def _cut_subword(tokens: List[str]) -> List[str]:
    _j = len(tokens)
    _i = 0
    while True:
        if _i == _j:
            break
        if (
            _RE_ENDING_CHAR.search(tokens[_i])
            and _i > 0
            and len(tokens[_i]) == 1
        ):
            tokens[_i - 1] += tokens[_i]
            del tokens[_i]
            _j -= 1
        _i += 1
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
    :return: list[str]
    """

    if not text or not isinstance(text, str):
        return []

    return _cut_subword(_cut_etcc.word_tokenize(text))
