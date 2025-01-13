# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenizers at different levels of linguistic analysis.
"""

__all__ = [
    "THAI2FIT_TOKENIZER",
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

from pythainlp.corpus import thai_syllables, thai_words
from pythainlp.util.trie import Trie

DEFAULT_WORD_TOKENIZE_ENGINE = "newmm"
DEFAULT_SENT_TOKENIZE_ENGINE = "crfcut"
DEFAULT_SUBWORD_TOKENIZE_ENGINE = "tcc"
DEFAULT_SYLLABLE_TOKENIZE_ENGINE = "han_solo"

DEFAULT_WORD_DICT_TRIE = Trie(thai_words())
DEFAULT_SYLLABLE_DICT_TRIE = Trie(thai_syllables())
DEFAULT_DICT_TRIE = DEFAULT_WORD_DICT_TRIE

from pythainlp.tokenize.core import (
    Tokenizer,
    paragraph_tokenize,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    word_detokenize,
    word_tokenize,
    display_cell_tokenize,
)

from pythainlp.corpus import get_corpus as _get_corpus

THAI2FIT_TOKENIZER = Tokenizer(
    custom_dict=_get_corpus("words_th_thai2fit_201810.txt"), engine="mm"
)
