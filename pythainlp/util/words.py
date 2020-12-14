# -*- coding: utf-8 -*-
"""
Tool for create word list
code is from Korakot Chaovavanich.

:See Also:
    * `Facebook post \
        <https://www.facebook.com/groups/colab.thailand/permalink/1667821073393244>`_
    * `Google Colab \
        <https://colab.research.google.com/drive/19kY2jCHONuxmTJM0U8PIE_I5OK1rO-x_>`_
"""

from collections import Counter
from typing import List
from pythainlp import word_tokenize, Tokenizer, corpus

def extract_pairs(words: List[str]) -> None:
  i = 0
  for w in words:
    yield i, i + len(w)
    i += len(w)

def create_wordlist(training_data: List[List[str]]) -> List[str]:
  right = Counter()
  wrong = Counter()
  for r_words in training_data:
    r_set = set(extract_pairs(r_words))
    t_words = word_tokenize(''.join(r_words))
    t_pairs = extract_pairs(t_words)
    for w, p in zip(t_words, t_pairs):
      if p in r_set:
        right[w] += 1
      else:
        wrong[w] += 1
  # after collect stat, remove bad words
  rem_words = []
  for w, v in wrong.items():
    if v > right[w]:
      rem_words.append(w)
  return sorted(set(corpus.thai_words()) - set(rem_words))