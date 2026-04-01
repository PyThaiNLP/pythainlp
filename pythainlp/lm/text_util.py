# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: C901
from __future__ import annotations


def calculate_ngram_counts(
    list_words: list[str], n_min: int = 2, n_max: int = 4
) -> dict[tuple[str, ...], int]:
    """Calculate n-gram counts for the given word list.

    :param list[str] list_words: list of words
    :param int n_min: minimum n-gram size (default: 2)
    :param int n_max: maximum n-gram size (default: 4)

    :return: dictionary mapping n-grams to their counts
    :rtype: dict[tuple[str, ...], int]
    """
    if not list_words:
        return {}

    ngram_counts: dict[tuple[str, ...], int] = {}

    for n in range(n_min, n_max + 1):
        for i in range(len(list_words) - n + 1):
            ngram = tuple(list_words[i : i + n])
            ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1

    return ngram_counts


def remove_repeated_ngrams(string_list: list[str], n: int = 2) -> list[str]:
    """Remove repeated n-grams from a word list.

    :param list[str] string_list: list of words
    :param int n: n-gram size
    :return: list of words with repeated n-grams removed
    :rtype: list[str]

    :Example:

        >>> from pythainlp.lm import remove_repeated_ngrams  # doctest: +SKIP

        >>> remove_repeated_ngrams(["เอา", "เอา", "แบบ", "ไหน"], n=1)  # doctest: +SKIP
        ['เอา', 'แบบ', 'ไหน']
    """
    if not string_list or n <= 0:
        return string_list

    unique_ngrams = set()

    output_list: list[str] = []

    for i in range(len(string_list)):
        if i + n <= len(string_list):
            ngram = tuple(string_list[i : i + n])

            if ngram not in unique_ngrams:
                unique_ngrams.add(ngram)

                if not output_list or output_list[-(n - 1) :] != list(
                    ngram[:-1]
                ):
                    output_list.extend(ngram)
                else:
                    output_list.append(ngram[-1])
        else:
            for char in string_list[i:]:
                if not output_list or output_list[-1] != char:
                    output_list.append(char)

    return output_list
