# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap AttaCut, a fast and reasonably accurate word tokenizer for Thai.

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
    """
    Tokenize text into words with AttaCut.

    The wrapper uses a lock to protect access to the internal tokenizer
    cache. However, thread-safety of the underlying AttaCut library itself
    is not guaranteed. Refer to the AttaCut library documentation for its
    thread-safety guarantees.

    :param str text: text to be tokenized
    :param str model: name of the AttaCut model.
        Options:

        * *attacut-sc* - (default) use both syllable and character features
        * *attacut-c* - use only character features

    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    # Thread-safe access to the tokenizers cache
    with _tokenizers_lock:
        if model not in _tokenizers:
            _tokenizers[model] = AttacutTokenizer(model)
        tokenizer = _tokenizers[model]

    return tokenizer.tokenize(text)
