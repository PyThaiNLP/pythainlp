# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Tool for creating word lists
codes are from Korakot Chaovavanich.

:See also:
    * `Facebook post \
        <https://www.facebook.com/groups/colab.thailand/permalink/1667821073393244>`_
    * `Google Colab \
        <https://colab.research.google.com/drive/19kY2jCHONuxmTJM0U8PIE_I5OK1rO-x_>`_
"""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

from pythainlp.corpus import thai_words
from pythainlp.tokenize import newmm
from pythainlp.util import Trie


def index_pairs(words: list[str]) -> Iterator[tuple[int, int]]:
    """Return beginning and ending indexes of word pairs"""
    i = 0
    for w in words:
        yield i, i + len(w)
        i += len(w)


def find_badwords(
    tokenize: Callable[[str], list[str]],
    training_data: Iterable[Iterable[str]],
) -> set[str]:
    """Find words that do not work well with the `tokenize` function
    for the provided `training_data`.

    :param Callable[[str], list[str]] tokenize: a tokenize function
    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: words that do not work well with the `tokenize` function
    :rtype: set[str]
    """
    right: Counter[str] = Counter()
    wrong: Counter[str] = Counter()

    for train_words in training_data:
        train_words_list = list(train_words)
        train_set = set(index_pairs(train_words_list))
        test_words = tokenize("".join(train_words_list))
        test_pairs = index_pairs(test_words)
        for w, p in zip(test_words, test_pairs):
            if p in train_set:
                right[w] += 1
            else:
                wrong[w] += 1

    # if wrong is more than right, then it's a bad word
    bad_words = []
    for w, count in wrong.items():
        if count > right[w]:
            bad_words.append(w)

    return set(bad_words)


def revise_wordset(
    tokenize: Callable[[str], list[str]],
    orig_words: Iterable[str],
    training_data: Iterable[Iterable[str]],
) -> set[str]:
    """Revise a set of words that could improve tokenization performance of
    a dictionary-based `tokenize` function.

    `orig_words` will be used as a base set for the dictionary.
    Words that do not perform well with `training_data` will be removed.
    The remaining words will be returned.

    :param Callable[[str], list[str]] tokenize: a tokenize function, can be\
        any function that takes a string as input and returns a list[str]
    :param Iterable[str] orig_words: words used by the tokenize function,\
        will be used as a base for revision
    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: revised set of words with underperforming words removed
    :rtype: set[str]

    :Example:

        >>> from pythainlp.corpus import thai_words  # doctest: +SKIP
        >>> from pythainlp.corpus.util import revise_wordset  # doctest: +SKIP
        >>> from pythainlp.tokenize.longest import segment  # doctest: +SKIP
        >>> base_words = thai_words()  # doctest: +SKIP
        >>> more_words = {  # doctest: +SKIP
        ...     "ถวิล อุดล", "ทองอินทร์ ภูริพัฒน์",
        ...     "เตียง ศิริขันธ์", "จำลอง ดาวเรือง",
        ... }
        >>> base_words = base_words.union(more_words)  # doctest: +SKIP
        >>> dict_trie = Trie(base_words)  # doctest: +SKIP
        >>> tokenize = lambda text: segment(text, dict_trie)  # doctest: +SKIP
        >>> training_data = [["word1", "word2"], ["word3", "word4"]]  # doctest: +SKIP
        >>> revised_words = revise_wordset(tokenize, base_words, training_data)  # doctest: +SKIP
    """
    bad_words = find_badwords(tokenize, training_data)
    return set(orig_words) - bad_words


def revise_newmm_default_wordset(
    training_data: Iterable[Iterable[str]],
) -> set[str]:
    """Revise a set of word that could improve tokenization performance of
    `pythainlp.tokenize.newmm`, a dictionary-based tokenizer and a default
    tokenizer for PyThaiNLP.

    Words from `pythainlp.corpus.thai_words()` will be used as a base set
    for the dictionary. Words that do not perform well with `training_data`
    will be removed. The remaining words will be returned.

    :param Iterable[Iterable[str]] training_data: tokenized text, to be used\
        as a training set
    :return: revised set of words with underperforming words removed
    :rtype: set[str]
    """
    orig_words = thai_words()
    trie = Trie(orig_words)

    def tokenize(text: str) -> list[str]:
        return newmm.segment(text, custom_dict=trie)

    revised_words = revise_wordset(tokenize, orig_words, training_data)
    return revised_words
