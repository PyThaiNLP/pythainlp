# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""

from __future__ import annotations

import threading
from typing import cast

from attacut import Tokenizer


class AttacutTokenizer:
    _MODEL_NAME: str
    _tokenizer: Tokenizer

    def __init__(self, model: str = "attacut-sc") -> None:
        self._MODEL_NAME: str = "attacut-sc"

        if model == "attacut-c":
            self._MODEL_NAME = "attacut-c"

        self._tokenizer: Tokenizer = Tokenizer(model=self._MODEL_NAME)

    def tokenize(self, text: str) -> list[str]:
        return cast("list[str]", self._tokenizer.tokenize(text))


_tokenizers: dict[str, AttacutTokenizer] = {}
_tokenizers_lock: threading.Lock = threading.Lock()


def segment(text: str, model: str = "attacut-sc") -> list[str]:
    """Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

    The wrapper uses a lock to protect access to the internal tokenizer cache.
    However, thread-safety of the underlying AttaCut library itself is not
    guaranteed. Please refer to the AttaCut library documentation for its
    thread-safety guarantees.

    :param str text: text to be tokenized to words
    :param str model: model of word tokenizer model
    :return: list of words, tokenized from the text
    :rtype: list[str]
    **Options for model**
        * *attacut-sc* (default) using both syllable and character features
        * *attacut-c* using only character feature
    """
    if not text or not isinstance(text, str):
        return []

    # Thread-safe access to the tokenizers cache
    with _tokenizers_lock:
        if model not in _tokenizers:
            _tokenizers[model] = AttacutTokenizer(model)
        tokenizer = _tokenizers[model]

    return tokenizer.tokenize(text)
