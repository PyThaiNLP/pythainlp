# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Provide tokenizer classes for ULMFiT."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection

from pythainlp.tokenize import thai2fit_tokenizer


class BaseTokenizer:
    """Provide a basic tokenizer interface (code from `fastai`)."""

    lang: str

    def __init__(self, lang: str) -> None:
        """Initialize tokenizer with a language code."""
        self.lang: str = lang

    def tokenizer(self, t: str) -> list[str]:
        """Split text on spaces."""
        return t.split(" ")

    def add_special_cases(self, toks: Collection[str]) -> None:
        """
        Accept special cases without changing this tokenizer.

        The fastai interface requires this hook, but this tokenizer has
        no custom special cases.
        """
        # The fastai interface requires this hook, but this tokenizer has
        # no custom special cases.


class ThaiTokenizer(BaseTokenizer):
    """Wrap the newmm tokenizer as a fastai tokenizer."""

    lang: str

    def __init__(self, lang: str = "th") -> None:
        """Initialize the tokenizer with a language code."""
        self.lang: str = lang

    @staticmethod
    def tokenizer(text: str) -> list[str]:
        """
        Tokenize text using the newmm engine and the thai2fit dictionary.

        :param str text: text to tokenize
        :return: tokenized text
        :rtype: list[str]

        :Example:

            Using :func:`ThaiTokenizer.tokenizer` is similar to
            :func:`pythainlp.tokenize.word_tokenize` with the
            ``"ulmfit"`` engine.

            >>> from pythainlp.lm.ulmfit import ThaiTokenizer
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
