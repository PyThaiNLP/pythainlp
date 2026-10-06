# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional

from pythainlp import thai_consonants
from pythainlp.transliterate import pronunciate

_list_consonants: list[str] = list(thai_consonants.replace("ห", ""))


def _initial_char(syllable: str) -> Optional[str]:
    """Return the first consonant of a syllable, or None if not found."""
    for char in syllable:
        if char in _list_consonants:
            return char
        if char == "ห" and "หฺ" not in syllable and len(syllable) == 2:
            return char
    return None


def _swap_two(pairs: list[tuple[str, str]]) -> list[str]:
    """Swap the initials of two syllables."""
    (syl_a, init_a), (syl_b, init_b) = pairs
    return [syl_b.replace(init_b, init_a, 1), syl_a.replace(init_a, init_b, 1)]


def _swap_three(pron: list[str], pairs: list[tuple[str, str]]) -> list[str]:
    """Swap the initials of the last two of three syllables."""
    _, (syl_b, init_b), (syl_c, init_c) = pairs
    return [
        pron[0],
        syl_c.replace(init_c, init_b, 1),
        syl_b.replace(init_b, init_c, 1),
    ]


def _swap_ends(pron: list[str], pairs: list[tuple[str, str]]) -> list[str]:
    """Swap the initials of the first and last syllables (4 or more)."""
    first = pron[0].replace(pairs[0][1], pairs[-1][1], 1)
    last = pron[-1].replace(pairs[-1][1], pairs[0][1], 1)
    return [first, *pron[1 : len(pairs) - 1], last]


def puan(word: str, show_pronunciation: bool = True) -> str:
    """Thai Spoonerism

    Converts a Thai word to a spoonerism word.

    :param str word: Thai word to be spoonerized
    :param bool show_pronunciation: True (default) or False

    :return: A string of Thai spoonerism word.
    :rtype: str

    :Example:

        >>> from pythainlp.transliterate import puan
        >>> puan("นาริน")  # doctest: +SKIP
        'นิน-รา'
        >>> puan("นาริน", False)  # doctest: +SKIP
        'นินรา'
    """
    word = pronunciate(word, engine="w2p")
    pron = word.split("-")
    if len(pron) == 1:
        return word

    initials = [c for c in map(_initial_char, pron) if c is not None]
    pairs = list(zip(pron, initials))
    if len(pairs) == 2:
        swapped = _swap_two(pairs)
    elif len(pairs) == 3:
        swapped = _swap_three(pron, pairs)
    else:  # > 3 syllables
        swapped = _swap_ends(pron, pairs)

    if not show_pronunciation:
        swapped = [i.replace("หฺ", "").replace("ฺ", "") for i in swapped]
    return ("-" if show_pronunciation else "").join(swapped)
