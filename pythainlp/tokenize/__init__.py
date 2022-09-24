# -*- coding: utf-8 -*-
"""
Tokenizers at different level of linguistic analysis.
"""

__all__ = [
    "THAI2FIT_TOKENIZER",
    "Tokenizer",
    "Trie",
    "clause_tokenize",
    "sent_tokenize",
    "subword_tokenize",
    "word_tokenize",
    "word_detokenize"
]

from pythainlp.corpus import thai_syllables, thai_words
from pythainlp.util.trie import Trie

DEFAULT_WORD_TOKENIZE_ENGINE = "newmm"
DEFAULT_SENT_TOKENIZE_ENGINE = "crfcut"
DEFAULT_SUBWORD_TOKENIZE_ENGINE = "tcc"
DEFAULT_SYLLABLE_TOKENIZE_ENGINE = "dict"

DEFAULT_WORD_DICT_TRIE = Trie(thai_words())
DEFAULT_SYLLABLE_DICT_TRIE = Trie(thai_syllables())
DEFAULT_DICT_TRIE = DEFAULT_WORD_DICT_TRIE

from pythainlp.tokenize.core import (
    Tokenizer,
    clause_tokenize,
    sent_tokenize,
    subword_tokenize,
    word_tokenize,
    word_detokenize,
)

from pythainlp.corpus import get_corpus as _get_corpus

THAI2FIT_TOKENIZER = Tokenizer(
    custom_dict=_get_corpus("words_th_thai2fit_201810.txt"), engine="newmm"
)
