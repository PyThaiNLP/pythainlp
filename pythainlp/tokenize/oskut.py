# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper OSKut (Out-of-domain StacKed cut for Word Segmentation).

Handling Cross- and Out-of-Domain Samples in Thai Word Segmentation
Stacked Ensemble Framework and DeepCut as Baseline model (ACL 2021 Findings).
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
    """Segment text using OSKut (via LEKCut ONNX).

    The wrapper uses a lock to protect access to the internal tokenizer cache.
    The model runs on ONNX runtime via LEKCut.

    :param str text: text to be tokenized
    :param str engine: model engine to use ("ws", "ws-augment-60p", "tnhc",
        "scads", "tl-deepcut-ws", "tl-deepcut-tnhc", or "deepcut")
    :return: list of tokens
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    with _tokenizers_lock:
        if engine not in _tokenizers:
            _tokenizers[engine] = OskutTokenizer(engine=engine)
        tokenizer = _tokenizers[engine]

    return cast("list[str]", tokenizer.tokenize(text))
