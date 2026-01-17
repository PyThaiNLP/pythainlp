# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for SEFR CUT Thai word segmentation. SEFR CUT is a
Thai Word Segmentation Models using Stacked Ensemble.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/SEFR_CUT>`_
"""

from __future__ import annotations

import threading

import sefr_cut

_DEFAULT_ENGINE = "ws1000"
_engine_lock = threading.Lock()

# Load default model at module initialization
sefr_cut.load_model(engine=_DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws1000") -> list[str]:
    """Segment text using SEFR CUT.

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
            sefr_cut.load_model(engine=_DEFAULT_ENGINE)

    return sefr_cut.tokenize(text)[0]
