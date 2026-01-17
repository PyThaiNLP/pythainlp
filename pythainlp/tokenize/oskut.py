# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper OSKut (Out-of-domain StacKed cut for Word Segmentation).
Handling Cross- and Out-of-Domain Samples in Thai Word Segmentation
Stacked Ensemble Framework and DeepCut as Baseline model (ACL 2021 Findings)

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/OSKut>`_
"""

from __future__ import annotations

import threading

import oskut

_DEFAULT_ENGINE = "ws"
_engine_lock = threading.Lock()

# Load default model at module initialization
oskut.load_model(engine=_DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws") -> list[str]:
    """Segment text using OSKut.

    This function is thread-safe. It uses a lock to protect model loading
    when switching engines.

    :param str text: text to be tokenized
    :param str engine: model engine to use
    :return: list of tokens
    """
    if not text or not isinstance(text, str):
        return []

    # Thread-safe model loading
    with _engine_lock:
        if engine != _DEFAULT_ENGINE:
            # Need to update global state and reload model
            global _DEFAULT_ENGINE
            _DEFAULT_ENGINE = engine
            oskut.load_model(engine=_DEFAULT_ENGINE)

    return oskut.OSKut(text)
