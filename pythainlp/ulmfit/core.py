# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Deprecated. Use :mod:`pythainlp.lm.ulmfit.core` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.ulmfit.core` has moved to :mod:`pythainlp.lm.ulmfit.core`.
"""

from __future__ import annotations

from pythainlp.lm.ulmfit.core import (
    THWIKI_LSTM,
    document_vector,
    get_thwiki_lstm,
    merge_wgts,
    post_rules_th,
    post_rules_th_sparse,
    pre_rules_th,
    pre_rules_th_sparse,
    process_thai,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.ulmfit.core",
    "pythainlp.lm.ulmfit.core",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "THWIKI_LSTM",
    "document_vector",
    "get_thwiki_lstm",
    "merge_wgts",
    "post_rules_th",
    "post_rules_th_sparse",
    "pre_rules_th",
    "pre_rules_th_sparse",
    "process_thai",
]
