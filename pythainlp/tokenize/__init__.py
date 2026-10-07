# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Tokenize Thai text at different levels of linguistic analysis."""

from __future__ import annotations

__all__: list[str] = [
    "Tokenizer",
    "Trie",
    "display_cell_tokenize",
    "paragraph_tokenize",
    "sent_tokenize",
    "subword_tokenize",
    "syllable_tokenize",
    "thai2fit_tokenizer",
    "word_detokenize",
    "word_tokenize",
]

from functools import lru_cache

from pythainlp.corpus import thai_syllables, thai_words
from pythainlp.util.trie import Trie

DEFAULT_WORD_TOKENIZE_ENGINE: str = "newmm"
DEFAULT_SENT_TOKENIZE_ENGINE: str = "crfcut"
DEFAULT_SUBWORD_TOKENIZE_ENGINE: str = "tcc"
DEFAULT_SYLLABLE_TOKENIZE_ENGINE: str = "han_solo"


@lru_cache
def word_dict_trie() -> Trie:
    """Return the default word trie, loaded lazily and cached."""
    return Trie(thai_words())


@lru_cache
def syllable_dict_trie() -> Trie:
    """Return the default syllable trie, loaded lazily and cached."""
    return Trie(thai_syllables())


from pythainlp.tokenize.core import (
    Tokenizer,
    display_cell_tokenize,
    paragraph_tokenize,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    word_detokenize,
    word_tokenize,
)
from pythainlp.tokenize.thai2fit import thai2fit_tokenizer
