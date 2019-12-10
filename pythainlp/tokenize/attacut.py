# -*- coding: utf-8 -*
"""
Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""
from typing import List

from attacut import tokenize


def segment(text: str) -> List[str]:
    """
    Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai
    :param str text: text to be tokenized to words
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    return tokenize(text)
