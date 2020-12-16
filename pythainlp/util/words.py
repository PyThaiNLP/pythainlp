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
from typing import List, Iterator, Tuple

from pythainlp import Tokenizer, corpus, word_tokenize


def extract_pairs(words: List[str]) -> Iterator[Tuple[int, int]]:
    """
    Return begining and ending index pairs of words
    """
    i = 0
    for w in words:
        yield i, i + len(w)
        i += len(w)


def create_wordlist(training_data: List[List[str]]) -> List[str]:
    """
    Create a word list based on pythainlp.corpus.thai_words()
    (a PyThaiNLP default Thai word list), substracting words that do not
    matched well with the provided training_data.
    """
    right = Counter()
    wrong = Counter()

    for train_words in training_data:
        train_set = set(extract_pairs(train_words))
        test_words = word_tokenize("".join(train_words))
        test_pairs = extract_pairs(test_words)
        for w, p in zip(test_words, test_pairs):
            if p in train_set:
                right[w] += 1
            else:
                wrong[w] += 1

    # if wrong more than right, then it's a bad word
    bad_words = []
    for w, count in wrong.items():
        if count > right[w]:
            bad_words.append(w)

    return sorted(set(corpus.thai_words()) - set(bad_words))
