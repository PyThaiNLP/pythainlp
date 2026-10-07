# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap SEFR CUT, a Thai word tokenizer.

SEFR CUT is a set of Thai word segmentation models that use a stacked
ensemble.
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
    """
    Tokenize text into words with SEFR CUT.

    The wrapper uses a lock to protect access to the internal tokenizer
    cache. The model runs on ONNX Runtime via LEKCut.

    :param str text: text to be tokenized
    :param str engine: name of the SEFR CUT model engine ("ws1000", "tnhc",
        or "best")
    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    with _tokenizers_lock:
        if engine not in _tokenizers:
            _tokenizers[engine] = SefrCutTokenizer(engine=engine)
        tokenizer = _tokenizers[engine]

    return cast("list[str]", tokenizer.tokenize(text))
