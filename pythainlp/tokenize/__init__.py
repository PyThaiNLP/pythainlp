# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenizers at different levels of linguistic analysis.
"""

__all__ = [
    "thai2fit_tokenizer",
    "Tokenizer",
    "Trie",
    "paragraph_tokenize",
    "sent_tokenize",
    "subword_tokenize",
    "syllable_tokenize",
    "word_detokenize",
    "word_tokenize",
    "display_cell_tokenize",
]

from functools import lru_cache

from pythainlp.corpus import thai_syllables, thai_words
from pythainlp.util.trie import Trie

DEFAULT_WORD_TOKENIZE_ENGINE = "newmm"
DEFAULT_SENT_TOKENIZE_ENGINE = "crfcut"
DEFAULT_SUBWORD_TOKENIZE_ENGINE = "tcc"
DEFAULT_SYLLABLE_TOKENIZE_ENGINE = "han_solo"


@lru_cache
def word_dict_trie():
    """Lazy load default word dict trie with cache"""
    return Trie(thai_words())


@lru_cache
def syllable_dict_trie():
    """Lazy load default syllable dict trie with cache"""
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
