# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    "syllable_tokenize",
    "word_tokenize",
    "word_detokenize",
    "paragraph_tokenize",
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
    clause_tokenize,
    sent_tokenize,
    subword_tokenize,
    syllable_tokenize,
    word_tokenize,
    word_detokenize,
    paragraph_tokenize,
)

from pythainlp.corpus import get_corpus as _get_corpus

THAI2FIT_TOKENIZER = Tokenizer(
    custom_dict=_get_corpus("words_th_thai2fit_201810.txt"), engine="newmm"
)
