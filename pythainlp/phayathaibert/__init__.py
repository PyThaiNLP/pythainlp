# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :mod:`pythainlp.lm.phayathaibert` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.phayathaibert` has moved to :mod:`pythainlp.lm.phayathaibert`.
"""

from __future__ import annotations

from pythainlp.lm.phayathaibert import (
    NamedEntityTagger,
    PartOfSpeechTagger,
    ThaiTextAugmenter,
    ThaiTextProcessor,
    segment,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.phayathaibert",
    "pythainlp.lm.phayathaibert",
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
