# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for SEFR CUT Thai word segmentation.

SEFR CUT is a Thai Word Segmentation Model using Stacked Ensemble.
SEFR CUT is ported to ONNX model using LEKCut.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/SEFR_CUT>`_
    * `LEKCut GitHub <https://github.com/PyThaiNLP/LEKCut>`_
"""

from __future__ import annotations

import threading
from typing import cast

from lekcut.sefrcut import SefrCutTokenizer

_tokenizers: dict[str, SefrCutTokenizer] = {}
_tokenizers_lock: threading.Lock = threading.Lock()


def segment(text: str, engine: str = "ws1000") -> list[str]:
    """Segment text using SEFR CUT (via LEKCut ONNX).

    The wrapper uses a lock to protect access to the internal tokenizer cache.
    The model runs on ONNX runtime via LEKCut.

    :param str text: text to be tokenized
    :param str engine: model engine to use ("ws1000", "tnhc", or "best")
    :return: list of tokens
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    with _tokenizers_lock:
        if engine not in _tokenizers:
            _tokenizers[engine] = SefrCutTokenizer(engine=engine)
        tokenizer = _tokenizers[engine]

    return cast("list[str]", tokenizer.tokenize(text))
