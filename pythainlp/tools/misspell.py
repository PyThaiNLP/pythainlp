# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import math
import random
from typing import Optional

THAI_CHARACTERS_WITHOUT_SHIFT: list[str] = [
    "ผปแอิืทมใฝ",
    "ฟหกดเ้่าสวง",
    "ๆไำพะัีรนยบลฃ",
    "ๅ/_ภถุึคตจขช",
]

THAI_CHARACTERS_WITH_SHIFT: list[str] = [
    "()ฉฮฺ์?ฒฬฦ",
    "ฤฆฏโฌ็๋ษศซ.",
    '๐"ฎฑธํ๊ณฯญฐ,',
    "+๑๒๓๔ู฿๕๖๗๘๙",
]

ENGLISH_CHARACTERS_WITHOUT_SHIFT: list[str] = [
    "1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./",
]

ENGLISH_CHARACTERS_WITH_SHIFT: list[str] = [
    "!@#$%^&*()_+",
    "QWERTYUIOP{}|",
    'ASDFGHJKL:"',
    "ZXCVBNM<>?",
]


ALL_CHARACTERS: list[list[str]] = [
    THAI_CHARACTERS_WITHOUT_SHIFT + THAI_CHARACTERS_WITH_SHIFT,
    ENGLISH_CHARACTERS_WITHOUT_SHIFT + ENGLISH_CHARACTERS_WITH_SHIFT,
]


def search_location_of_character(
    char: str,
) -> Optional[tuple[int, int, int, int]]:
    for language_ix in [0, 1]:
        for ix, row in enumerate(ALL_CHARACTERS[language_ix]):
            if char in row:
                return (language_ix, ix // 4, ix % 4, row.index(char))
    return None


def find_neighbour_locations(
    loc: tuple[int, int, int, int],
    char: str,
    kernel: list[tuple[int, int]] = [
        (-1, -1),
        (-1, 0),
        (1, 1),
        (0, 1),
        (0, -1),
        (1, 0),
    ],
) -> list[tuple[int, int, int, int, str]]:
    language_ix, is_shift, row, pos = loc

    valid_neighbours = []
    for kr, ks in kernel:
        _row, _pos = row + kr, pos + ks
        if 0 <= _row <= 3 and 0 <= _pos <= len(
            ALL_CHARACTERS[language_ix][is_shift * 4 + _row]
        ):
            valid_neighbours.append((language_ix, is_shift, _row, _pos, char))

    return valid_neighbours


def find_misspell_candidates(
    char: str, verbose: bool = False
) -> Optional[list[str]]:
    loc = search_location_of_character(char)
    if loc is None:
        return None

    valid_neighbours = find_neighbour_locations(loc, char)

    chars = []
    printing_locations = ["▐"] * 3 + [char] + ["▐"] * 3

    for language_ix, is_shift, row, pos, char in valid_neighbours:
        try:
            char = ALL_CHARACTERS[language_ix][is_shift * 4 + row][pos]
            chars.append(char)
            kernel = (row - loc[1], pos - loc[2])

            if kernel == (-1, -1):
                ix = 5
            elif kernel == (-1, 0):
                ix = 6
            elif kernel[0] == 0:
                ix = 3 + kernel[1]
            elif kernel == (1, 0):
                ix = 0
            elif kernel == (1, 1):
                ix = 1
            else:
                continue
            printing_locations[ix] = char
        except IndexError:
            continue
        except Exception:
            print("Something wrong with: ", char)
            raise

    return chars


def misspell(sentence: str, ratio: float = 0.05) -> str:
    """Simulate some misspellings of the input sentence.
    The number of misspelled locations is governed by ratio.

    :params str sentence: sentence to be misspelled
    :params float ratio: number of misspells per 100 chars. Defaults to 0.5.

    :return: sentence containing some misspelled words
    :rtype: str

    :Example:

        >>> from pythainlp.tools.misspell import misspell  # doctest: +SKIP
        >>> sentence = "ภาษาไทยปรากฏครั้งแรกในพุทธศักราช 1826"  # doctest: +SKIP
        >>> misspell(sentence, ratio=0.1)  # doctest: +SKIP
        'ภาษาไทยปรากฏครั้งแรกในกุทธศักราช 1727'
    """
    num_misspells = math.floor(len(sentence) * ratio)
    positions = random.sample(range(len(sentence)), k=num_misspells)

    # convert strings to array of characters
    misspelled = list(sentence)
    for pos in positions:
        potential_candidates = find_misspell_candidates(sentence[pos])
        if potential_candidates is None:
            continue

        # Non-cryptographic use, pseudo-random generator is acceptable here
        candidate = random.choice(potential_candidates)  # noqa: S311

        misspelled[pos] = candidate

    return "".join(misspelled)
