# -*- coding: utf-8 -*-
"""
Tokenzier classes for ULMFiT
"""

from typing import Collection, List
from pythainlp.tokenize import THAI2FIT_TOKENIZER


class BaseTokenizer:
    """Basic class for a tokenizer function. (code from `fastai`)"""

    def __init__(self, lang: str):
        self.lang = lang

    def tokenizer(self, t: str) -> List[str]:
        return t.split(" ")

    def add_special_cases(self, toks: Collection[str]):
        pass


class ThaiTokenizer(BaseTokenizer):
    """
    Wrapper around a frozen newmm tokenizer to make it a
    :class:`fastai.BaseTokenizer`.
    (see: https://docs.fast.ai/text.transform#BaseTokenizer)
    """

    def __init__(self, lang: str = "th"):
        self.lang = lang

    @staticmethod
    def tokenizer(text: str) -> List[str]:
        """
        This function tokenizes text with *newmm* engine and the dictionary
        specifically for `ulmfit` related functions
        (see: `Dictonary file (.txt) \
        <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th_thai2fit_201810.txt>`_).
        :meth: tokenize text with a frozen newmm engine
        :param str text: text to tokenize
        :return: tokenized text
        :rtype: list[str]

        :Example:

            Using :func:`pythainlp.ulmfit.ThaiTokenizer.tokenizer` is
            similar to :func:`pythainlp.tokenize.word_tokenize`
            with *ulmfit* engine.

            >>> from pythainlp.ulmfit import ThaiTokenizer
            >>> from pythainlp.tokenize import word_tokenize
            >>>
            >>> text = "อาภรณ์, จินตมยปัญญา ภาวนามยปัญญา"
            >>> ThaiTokenizer.tokenizer(text)
             ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']
            >>>
            >>> word_tokenize(text, engine='ulmfit')
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']

        """
        return THAI2FIT_TOKENIZER.word_tokenize(text)

    def add_special_cases(self, toks):
        pass
