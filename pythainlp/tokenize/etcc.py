# -*- coding: utf-8 -*-
"""
Enhanced Thai Character Cluster (ETCC)
Python implementation by Wannaphong Phatthiyaphaibun

Notebook : https://colab.research.google.com/drive/1UTQgxxMRxOr9Jp1B1jcq1frBNvorhtBQ

:See Also:

Inrut, Jeeragone, Patiroop Yuanghirun, Sarayut Paludkong, Supot Nitsuwat, and Para Limmaneepraserth.
"Thai word segmentation using combination of forward and backward longest matching techniques."
In International Symposium on Communications and Information Technology (ISCIT), pp. 37-40. 2001.
"""

import re
from typing import List
from pythainlp.tokenize import Tokenizer,Trie
from pythainlp.corpus import get_corpus
_etcc_trie = Trie(list(get_corpus("etcc.dict")))
_cut_etcc = Tokenizer(_etcc_trie, engine='longest')

def _cut_subword(listword: list) -> List[str]:
  _j = len(listword)
  _i = 0
  while True:
    if _i == _j:
      break
    if (re.search("[ะาๆฯๅำ]", listword[_i]) 
    and _i > 0 
    and len(listword[_i]) == 1):
      listword[_i - 1] += listword[_i]
      del listword[_i]
      _j -= 1
    _i += 1
  return listword

def segment(text: str) -> List[str]:
    """
    Enhanced Thai Character Cluster (ETCC)

    :param string text: word input

    :return: etcc
    """

    if not text or not isinstance(text, str):
        return ""

    return _cut_subword(_cut_etcc.word_tokenize(text))
