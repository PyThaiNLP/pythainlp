# -*- coding: utf-8 -*
"""
Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""
from typing import List

from attacut import Tokenizer
_MODEL_NAME = "attacut-sc"
_tokenize = Tokenizer(model=_MODEL_NAME)

def segment(text: str, model: str = "attacut-sc") -> List[str]:
    """
    Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai
    :param str text: text to be tokenized to words
    :param str model:  word tokenizer model to be tokenized to words
    :return: list of words, tokenized from the text
    :rtype: list[str]
    **Options for model**
        * *attacut-sc* (default)
        * *attacut-c*
    """
    if not text or not isinstance(text, str):
        return []

    if model != _MODEL_NAME:
        _MODEL_NAME = model
        _tokenize = Tokenizer(model=_MODEL_NAME)

    return _tokenize.tokenize(text)
