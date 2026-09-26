# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :mod:`pythainlp.lm.wangchanberta.core` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.wangchanberta.core` has moved to :mod:`pythainlp.lm.wangchanberta.core`.
"""

from __future__ import annotations

from pythainlp.lm.wangchanberta.core import (
    NamedEntityRecognition,
    ThaiNameTagger,
    segment,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.wangchanberta.core",
    "pythainlp.lm.wangchanberta.core",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "NamedEntityRecognition",
    "ThaiNameTagger",
    "segment",
]
