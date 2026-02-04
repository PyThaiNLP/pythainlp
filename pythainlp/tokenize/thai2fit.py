# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

from functools import lru_cache

from pythainlp.corpus import get_corpus
from pythainlp.tokenize import Tokenizer


@lru_cache
def thai2fit_tokenizer() -> Tokenizer:
    """Lazy load Thai2Fit tokenizer with cache"""
    return Tokenizer(
        custom_dict=get_corpus("words_th_thai2fit_201810.txt"), engine="mm"
    )
