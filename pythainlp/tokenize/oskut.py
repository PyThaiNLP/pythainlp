# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap OSKut (Out-of-domain StacKed cut for Word Segmentation).

OSKut is described in "Handling Cross- and Out-of-Domain Samples in Thai
Word Segmentation" (ACL 2021 Findings). It uses a stacked ensemble
framework with DeepCut as the baseline model.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/OSKut>`_
"""

from __future__ import annotations

import threading
from typing import cast

import oskut

_DEFAULT_ENGINE: str = "ws"
_engine_lock: threading.Lock = threading.Lock()

# Load default model at module initialization
oskut.load_model(engine=_DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws") -> list[str]:
    """
    Tokenize text into words with OSKut.

    The wrapper uses a lock to protect model loading when switching engines.
    However, thread-safety of the underlying OSKut library itself is not
    guaranteed. Refer to the OSKut library documentation for its
    thread-safety guarantees.

    :param str text: text to be tokenized
    :param str engine: name of the OSKut model engine
    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    # Thread-safe model loading
    global _DEFAULT_ENGINE
    with _engine_lock:
        if engine != _DEFAULT_ENGINE:
            # Need to update global state and reload model
            _DEFAULT_ENGINE = engine
            oskut.load_model(engine=_DEFAULT_ENGINE)

    return cast("list[str]", oskut.OSKut(text))
