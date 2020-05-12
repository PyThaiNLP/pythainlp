# -*- coding: utf-8 -*-
"""
thai2fit - Thai word vector.

Initial code from https://github.com/cstorm125/thai2fit
"""
__all__ = [
    "doesnt_match",
    "get_model",
    "most_similar_cosmul",
    "sentence_vectorizer",
    "similarity",
]

from pythainlp.word_vector.core import (
    doesnt_match,
    get_model,
    most_similar_cosmul,
    sentence_vectorizer,
    similarity,
)
