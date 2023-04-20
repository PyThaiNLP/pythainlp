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
Tool for create word list
code is from Korakot Chaovavanich.

:See also:
    * `Facebook post \
        <https://www.facebook.com/groups/colab.thailand/permalink/1667821073393244>`_
    * `Google Colab \
        <https://colab.research.google.com/drive/19kY2jCHONuxmTJM0U8PIE_I5OK1rO-x_>`_
"""

from collections import Counter
from typing import Callable, Iterable, Iterator, List, Set, Tuple

from pythainlp.corpus import thai_words
from pythainlp.tokenize import newmm
from pythainlp.util import Trie


def index_pairs(words: List[str]) -> Iterator[Tuple[int, int]]:
    """
    Return begining and ending index pairs of words
    """
    i = 0
    for w in words:
        yield i, i + len(w)
        i += len(w)


def find_badwords(
    tokenize: Callable[[str], List[str]],
    training_data: Iterable[Iterable[str]],
) -> Set[str]:
    """
    Find words that do not work well with the `tokenize` function
    for the provided `training_data`.

    :param Callable[[str], List[str]] tokenize: a tokenize function
    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: words that considered making `tokenize` perform unwell
    :rtype: Set[str]
    """
    right = Counter()
    wrong = Counter()

    for train_words in training_data:
        train_set = set(index_pairs(train_words))
        test_words = tokenize("".join(train_words))
        test_pairs = index_pairs(test_words)
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

    return set(bad_words)


def revise_wordset(
    tokenize: Callable[[str], List[str]],
    orig_words: Iterable[str],
    training_data: Iterable[Iterable[str]],
) -> Set[str]:
    """
    Revise a set of word that could improve tokenization performance of
    a dictionary-based `tokenize` function.

    `orign_words` will be used as a base set for the dictionary.
    Words that do not performed well with `training_data` will be removed.
    The remaining words will be returned.

    :param Callable[[str], List[str]] tokenize: a tokenize function, can be\
        any function that takes a string as input and returns a List[str]
    :param Iterable[str] orig_words: words that used by the tokenize function,\
        will be used as a base for revision
    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: words that considered making `tokenize` perform unwell
    :rtype: Set[str]

    :Example::
    ::

    from pythainlp.corpus import thai_words
    from pythainlp.corpus.util import revise_wordset
    from pythainlp.tokenize.longest import segment

    base_words = thai_words()
    more_words = {
        "ถวิล อุดล", "ทองอินทร์ ภูริพัฒน์", "เตียง ศิริขันธ์", "จำลอง ดาวเรือง"
    }
    base_words = base_words.union(more_words)
    dict_trie = Trie(wordlist)

    tokenize = lambda text: segment(text, dict_trie)

    training_data = [
        [str, str, str. ...],
        [str, str, str, str, ...],
        ...
    ]

    revised_words = revise_wordset(tokenize, wordlist, training_data)
    """
    bad_words = find_badwords(tokenize, training_data)
    return set(orig_words) - bad_words


def revise_newmm_default_wordset(
    training_data: Iterable[Iterable[str]],
) -> Set[str]:
    """
    Revise a set of word that could improve tokenization performance of
    `pythainlp.tokenize.newmm`, a dictionary-based tokenizer and a default
    tokenizer for PyThaiNLP.

    Words from `pythainlp.corpus.thai_words()` will be used as a base set
    for the dictionary. Words that do not performed well with `training_data`
    will be removed. The remaining words will be returned.

    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: words that considered making `tokenize` perform unwell
    :rtype: Set[str]
    """
    orig_words = thai_words()
    trie = Trie(orig_words)

    def tokenize(text):
        return newmm.segment(text, custom_dict=trie)

    revised_words = revise_wordset(tokenize, orig_words, training_data)
    return revised_words
