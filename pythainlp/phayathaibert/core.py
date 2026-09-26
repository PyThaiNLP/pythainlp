# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :mod:`pythainlp.lm.phayathaibert.core` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.phayathaibert.core` has moved to :mod:`pythainlp.lm.phayathaibert.core`.
"""

from __future__ import annotations

from pythainlp.lm.phayathaibert.core import (
    NamedEntityTagger,
    PartOfSpeechTagger,
    ThaiTextAugmenter,
    ThaiTextProcessor,
    segment,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.phayathaibert.core",
    "pythainlp.lm.phayathaibert.core",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "NamedEntityTagger",
    "PartOfSpeechTagger",
    "ThaiTextAugmenter",
    "ThaiTextProcessor",
    "segment",
]
