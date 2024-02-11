# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List
import numpy as np

THAI_CHARACTERS_WITHOUT_SHIFT = [
    "ผปแอิืทมใฝ",
    "ฟหกดเ้่าสวง",
    "ๆไำพะัีรนยบลฃ",
    "ๅ/_ภถุึคตจขช",
]

THAI_CHARACTERS_WITH_SHIFT = [
    "()ฉฮฺ์?ฒฬฦ",
    "ฤฆฏโฌ็๋ษศซ.",
    '๐"ฎฑธํ๊ณฯญฐ,',
    "+๑๒๓๔ู฿๕๖๗๘๙",
]

ENGLISH_CHARACTERS_WITHOUT_SHIFT = [
    "1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./",
]

ENGLISH_CHARACTERS_WITH_SHIFT = [
    "!@#$%^&*()_+",
    "QWERTYUIOP{}|",
    'ASDFGHJKL:"',
    "ZXCVBNM<>?",
]


ALL_CHARACTERS = [
    THAI_CHARACTERS_WITHOUT_SHIFT + THAI_CHARACTERS_WITH_SHIFT,
    ENGLISH_CHARACTERS_WITHOUT_SHIFT + ENGLISH_CHARACTERS_WITH_SHIFT,
]


def search_location_of_character(char: str):
    for language_ix in [0, 1]:
        for ix, row in enumerate(ALL_CHARACTERS[language_ix]):
            if char in row:
                return (language_ix, ix // 4, ix % 4, row.index(char))


def find_neighbour_locations(
    loc: tuple,
    char: str,
    kernel: List = [(-1, -1), (-1, 0), (1, 1), (0, 1), (0, -1), (1, 0)],
):
    language_ix, is_shift, row, pos = loc

    valid_neighbours = []
    for kr, ks in kernel:
        _row, _pos = row + kr, pos + ks
        if 0 <= _row <= 3 and 0 <= _pos <= len(
            ALL_CHARACTERS[language_ix][is_shift * 4 + _row]
        ):
            valid_neighbours.append((language_ix, is_shift, _row, _pos, char))

    return valid_neighbours


def find_misspell_candidates(char: str, verbose: bool = False):
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
        except Exception as e:
            print("Something wrong with: ", char)
            raise e

    return chars


def misspell(sentence: str, ratio: float = 0.05):
    """
    Simulate some misspellings of the input sentence.
    The number of misspelled locations is governed by ratio.

    :params str sentence: sentence to be misspelled
    :params float ratio: number of misspells per 100 chars. Defaults to 0.5.

    :return: sentence containing some misspelled words
    :rtype: str

    :Example:
    ::

        from pythainlp.tools.misspell import misspell

        sentence = "ภาษาไทยปรากฏครั้งแรกในพุทธศักราช 1826"

        misspell(sent, ratio=0.1)
        # output:
        ภาษาไทยปรากฏครั้งแรกในกุทธศักราช 1727
    """
    num_misspells = np.floor(len(sentence) * ratio).astype(int)
    positions = np.random.choice(
        len(sentence), size=num_misspells, replace=False
    )

    # convert strings to array of characters
    misspelled = list(sentence)
    for pos in positions:
        potential_candidates = find_misspell_candidates(sentence[pos])
        if potential_candidates is None:
            continue

        candidate = np.random.choice(potential_candidates)

        misspelled[pos] = candidate

    return "".join(misspelled)
