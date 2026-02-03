# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Tokenzier classes for ULMFiT"""

from __future__ import annotations

from collections.abc import Collection

from pythainlp.tokenize import thai2fit_tokenizer


class BaseTokenizer:
    """Basic class for a tokenizer function. (codes from `fastai`)"""

    lang: str

    def __init__(self, lang: str) -> None:
        self.lang: str = lang

    def tokenizer(self, t: str) -> list[str]:
        return t.split(" ")

    def add_special_cases(self, toks: Collection[str]) -> None:
        pass


class ThaiTokenizer(BaseTokenizer):
    """Wrapper around a frozen newmm tokenizer to make it a
    :class:`fastai.BaseTokenizer`.
    (see: https://docs.fast.ai/text.transform#BaseTokenizer)
    """

    lang: str

    def __init__(self, lang: str = "th") -> None:
        self.lang: str = lang

    @staticmethod
    def tokenizer(text: str) -> list[str]:
        """This function tokenizes text using *newmm* engine and the dictionary
        specifically for `ulmfit` related functions
        (see: `Dictionary file (.txt) \
        <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th_thai2fit_201810.txt>`_).
        :meth: tokenize text using a frozen newmm engine
        :param str text: text to tokenize
        :return: tokenized text
        :rtype: list[str]

        :Example:

            Using :func:`pythainlp.ulmfit.ThaiTokenizer.tokenizer` is
            similar to :func:`pythainlp.tokenize.word_tokenize`
            using *ulmfit* engine.

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
        return thai2fit_tokenizer().word_tokenize(text)  # type: ignore[no-any-return]

    def add_special_cases(self, toks: Collection[str]) -> None:
        pass
