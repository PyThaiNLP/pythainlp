# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap AttaCut, a fast and reasonably accurate word tokenizer for Thai.

AttaCut is ported to ONNX model using LEKCut.

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
    * `LEKCut GitHub <https://github.com/PyThaiNLP/LEKCut>`_
"""

from __future__ import annotations

import threading
from typing import cast

from lekcut.attacut import tokenize as lekcut_tokenize


class AttacutTokenizer:
    """Wrap the AttaCut tokenizer."""

    _MODEL_NAME: str

    def __init__(self, model: str = "attacut-sc") -> None:
        """
        Initialize the AttaCut tokenizer.

        :param str model: name of the AttaCut model (attacut-sc or attacut-c)
        """
        self._MODEL_NAME: str = "attacut-sc"

        if model == "attacut-c":
            self._MODEL_NAME = "attacut-c"

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into words.

        :param str text: text to be tokenized
        :return: list of words
        :rtype: list[str]
        """
        if not text or not isinstance(text, str):
            return []
        return cast("list[str]", lekcut_tokenize(text, model=self._MODEL_NAME))


_tokenizers: dict[str, AttacutTokenizer] = {}
_tokenizers_lock: threading.Lock = threading.Lock()


def segment(text: str, model: str = "attacut-sc") -> list[str]:
    """
    Tokenize text into words with AttaCut.

    The wrapper uses a lock to protect access to the internal tokenizer
    cache. The model runs on ONNX Runtime via LEKCut.

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
