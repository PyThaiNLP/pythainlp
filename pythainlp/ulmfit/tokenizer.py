# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Tokenizer classes for ULMFiT."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection

from pythainlp.tokenize import thai2fit_tokenizer


class BaseTokenizer:
    """Provide a basic tokenizer class (code from `fastai`)."""

    lang: str

    def __init__(self, lang: str) -> None:
        self.lang: str = lang

    def tokenizer(self, t: str) -> list[str]:
        return t.split(" ")

    def add_special_cases(self, toks: Collection[str]) -> None:
        pass


class ThaiTokenizer(BaseTokenizer):
    """
    Wrap a frozen newmm tokenizer as a :class:`fastai.BaseTokenizer`.

    See https://docs.fast.ai/text.transform#BaseTokenizer
    """

    lang: str

    def __init__(self, lang: str = "th") -> None:
        self.lang: str = lang

    @staticmethod
    def tokenizer(text: str) -> list[str]:
        """
        Tokenize text using the newmm engine and the thai2fit dictionary.

        :param str text: text to be tokenized
        :return: list of words
        :rtype: list[str]

        :Example:

            Using :func:`ThaiTokenizer.tokenizer` is similar to
            :func:`pythainlp.tokenize.word_tokenize` with the
            ``"ulmfit"`` engine.

            >>> from pythainlp.ulmfit import ThaiTokenizer
            >>> from pythainlp.tokenize import word_tokenize
            >>>
            >>> text = "อาภรณ์, จินตมยปัญญา ภาวนามยปัญญา"
            >>> ThaiTokenizer.tokenizer(text)
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']
            >>>
            >>> word_tokenize(text, engine="ulmfit")
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']

        """
        return thai2fit_tokenizer().word_tokenize(text)

    def add_special_cases(self, toks: Collection[str]) -> None:
        pass
