# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap SEFR CUT, a Thai word tokenizer.

SEFR CUT is a set of Thai word segmentation models that use a stacked
ensemble.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/SEFR_CUT>`_
"""

from __future__ import annotations

import threading
from typing import cast

import sefr_cut

_DEFAULT_ENGINE: str = "ws1000"
_engine_lock: threading.Lock = threading.Lock()

# Load default model at module initialization
sefr_cut.load_model(engine=_DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws1000") -> list[str]:
    """
    Tokenize text into words with SEFR CUT.

    The wrapper uses a lock to protect model loading when switching engines.
    However, thread-safety of the underlying SEFR CUT library itself is not
    guaranteed. Refer to the SEFR CUT library documentation for its
    thread-safety guarantees.

    :param str text: text to be tokenized
    :param str engine: name of the SEFR CUT model engine
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
            sefr_cut.load_model(engine=_DEFAULT_ENGINE)

    return cast("list[str]", sefr_cut.tokenize(text)[0])
