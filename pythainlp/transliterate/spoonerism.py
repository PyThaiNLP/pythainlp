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


def _swap_initials(pron: list[str]) -> list[str]:
    """Swap initials or rimes of syllables, keeping every position.

    With 2 or 3 syllables that have an initial, the last two swap their
    rimes while the initials stay. With 4 or more, the initials of the
    first and last swap. Syllables without an initial stay in place.
    """
    found = [
        (i, c) for i, c in enumerate(map(_initial_char, pron)) if c is not None
    ]
    swapped = list(pron)
    if len(found) < 2:
        return swapped
    if len(found) <= 3:  # 2 or 3: the last two swap rimes, initials stay
        (i, a), (j, b) = found[-2:]
        swapped[i] = pron[j].replace(b, a, 1)
        swapped[j] = pron[i].replace(a, b, 1)
    else:  # 4 or more: swap the initials of the first and last
        (i, a), (j, b) = found[0], found[-1]
        swapped[i] = pron[i].replace(a, b, 1)
        swapped[j] = pron[j].replace(b, a, 1)
    return swapped


def puan(word: str, show_pronunciation: bool = True) -> str:
    """Thai Spoonerism

    Converts a Thai word to a spoonerism word.

    Syllables without an initial consonant stay in place.

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

    swapped = _swap_initials(pron)

    if not show_pronunciation:
        swapped = [i.replace("หฺ", "").replace("ฺ", "") for i in swapped]
    return ("-" if show_pronunciation else "").join(swapped)
