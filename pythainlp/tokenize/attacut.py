# -*- coding: utf-8 -*
"""
Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""
from typing import List

from attacut import Tokenizer


class attacut:
    def __init__(self, model= "attacut-sc"):
        if model == "attacut-sc":
            self.load_attacut_sc()
        else:
            self.load_attacut_c()
    def tokenize(self,text:str) -> List[str]:
        return self._tokenizer.tokenize(text)
    def load_attacut_sc(self):
        self._MODEL_NAME = "attacut-sc"
        self._tokenizer = Tokenizer(model=self._MODEL_NAME)
    def load_attacut_c(self):
        self._MODEL_NAME = "attacut-c"
        self._tokenizer = Tokenizer(model=self._MODEL_NAME)


def segment(text: str, model: str = "attacut-sc") -> List[str]:
    """
    Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai
    :param str text: text to be tokenized to words
    :param str model:  word tokenizer model to be tokenized to words
    :return: list of words, tokenized from the text
    :rtype: list[str]
    **Options for model**
        * *attacut-sc* (default) using both syllable and character features
        * *attacut-c* using only character feature
    """
    if not text or not isinstance(text, str):
        return []

    _tokenizer = attacut(model)

    return _tokenizer.tokenize(text)
