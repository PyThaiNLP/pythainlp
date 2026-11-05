# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Deprecated. Use :mod:`pythainlp.lm.ulmfit.tokenizer` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.ulmfit.tokenizer` has moved to :mod:`pythainlp.lm.ulmfit.tokenizer`.
"""

from __future__ import annotations

from pythainlp.lm.ulmfit.tokenizer import (
    BaseTokenizer,
    ThaiTokenizer,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.ulmfit.tokenizer",
    "pythainlp.lm.ulmfit.tokenizer",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "BaseTokenizer",
    "ThaiTokenizer",
]
