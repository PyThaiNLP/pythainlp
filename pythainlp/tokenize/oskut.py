# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap OSKut (Out-of-domain StacKed cut for Word Segmentation).

OSKut is described in "Handling Cross- and Out-of-Domain Samples in Thai
Word Segmentation" (ACL 2021 Findings). It uses a stacked ensemble
framework with DeepCut as the baseline model.
OSKut is ported to ONNX model using LEKCut.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/OSKut>`_
    * `LEKCut GitHub <https://github.com/PyThaiNLP/LEKCut>`_
"""

from __future__ import annotations

import threading
from typing import cast

from lekcut.oskut import OskutTokenizer

_tokenizers: dict[str, OskutTokenizer] = {}
_tokenizers_lock: threading.Lock = threading.Lock()


def segment(text: str, engine: str = "ws") -> list[str]:
    """
    Tokenize text into words with OSKut.

    The wrapper uses a lock to protect access to the internal tokenizer
    cache. The model runs on ONNX Runtime via LEKCut.

    :param str text: text to be tokenized
    :param str engine: name of the OSKut model engine ("ws", "ws-augment-60p",
        "tnhc", "scads", "tl-deepcut-ws", "tl-deepcut-tnhc", or "deepcut")
    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    with _tokenizers_lock:
        if engine not in _tokenizers:
            _tokenizers[engine] = OskutTokenizer(engine=engine)
        tokenizer = _tokenizers[engine]

    return cast("list[str]", tokenizer.tokenize(text))
