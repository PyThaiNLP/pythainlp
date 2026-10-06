# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Longest common subsequence functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def _lcs_lengths(str1: Sequence[str], str2: Sequence[str]) -> list[list[int]]:
    """
    Build the table of longest common subsequence lengths.

    ``table[i][j]`` is the length for ``str1[:i]`` and ``str2[:j]``.
    Each argument is a string or another sequence of strings.
    """
    m = len(str1)
    n = len(str2)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def longest_common_subsequence(str1: str, str2: str) -> str:
    """
    Return the longest common subsequence of two strings.

    :param str str1: first string
    :param str str2: second string
    :return: longest common subsequence
    :rtype: str

    :Example:

        >>> from pythainlp.util.lcs import longest_common_subsequence
        >>> longest_common_subsequence("ABCBDAB", "BDCAB")
        'BDAB'
    """
    table = _lcs_lengths(str1, str2)

    # Walk back from the bottom-right corner and collect the matches.
    chars: list[str] = []
    i = len(str1)
    j = len(str2)
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            chars.append(str1[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] > table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(chars))
