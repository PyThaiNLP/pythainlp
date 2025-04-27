# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
symspellpy

symspellpy is a Python port of SymSpell v6.5.
We used unigram & bigram from Thai National Corpus (TNC).

:See Also:
    * \
        https://github.com/mammothb/symspellpy
"""

from typing import List

try:
    from symspellpy import SymSpell, Verbosity
except ImportError:
    raise ImportError("Import Error; Install symspellpy by pip install symspellpy")

from pythainlp.corpus import get_corpus_path, path_pythainlp_corpus

_UNIGRAM_FILENAME = "tnc_freq.txt"
_BIGRAM_CORPUS_NAME = "tnc_bigram_word_freqs"

sym_spell = SymSpell()
sym_spell.load_dictionary(
    path_pythainlp_corpus(_UNIGRAM_FILENAME),
    0,
    1,
    separator="\t",
    encoding="utf-8-sig",
)
sym_spell.load_bigram_dictionary(
    get_corpus_path(_BIGRAM_CORPUS_NAME),
    0,
    2,
    separator="\t",
    encoding="utf-8-sig",
)


def spell(text: str, max_edit_distance: int = 2) -> List[str]:
    return [
        str(i).split(",", maxsplit=1)[0]
        for i in list(
            sym_spell.lookup(
                text, Verbosity.CLOSEST, max_edit_distance=max_edit_distance
            )
        )
    ]


def correct(text: str, max_edit_distance: int = 1) -> str:
    return spell(text, max_edit_distance=max_edit_distance)[0]


def spell_sent(
    list_words: List[str], max_edit_distance: int = 2
) -> List[List[str]]:
    temp = [
        str(i).split(",", maxsplit=1)[0].split(" ")
        for i in list(
            sym_spell.lookup_compound(
                " ".join(list_words),
                split_by_space=True,
                max_edit_distance=max_edit_distance,
            )
        )
    ]
    list_new = []
    for i in temp:
        list_new.append(i)

    return list_new


def correct_sent(list_words: List[str], max_edit_distance=1) -> List[str]:
    return [
        i[0]
        for i in spell_sent(list_words, max_edit_distance=max_edit_distance)
    ]
