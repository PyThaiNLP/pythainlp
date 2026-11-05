# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Deprecated. Use :mod:`pythainlp.lm.ulmfit` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.ulmfit` has moved to :mod:`pythainlp.lm.ulmfit`.
"""

from __future__ import annotations

from pythainlp.lm.ulmfit import (
    THWIKI_LSTM,
    ThaiTokenizer,
    document_vector,
    fix_html,
    get_thwiki_lstm,
    lowercase_all,
    merge_wgts,
    post_rules_th,
    post_rules_th_sparse,
    pre_rules_th,
    pre_rules_th_sparse,
    process_thai,
    remove_space,
    replace_rep_after,
    replace_rep_nonum,
    replace_url,
    replace_wrep_post,
    replace_wrep_post_nonum,
    rm_brackets,
    rm_useless_newlines,
    rm_useless_spaces,
    spec_add_spaces,
    ungroup_emoji,
)
from pythainlp.tools import warn_deprecation

warn_deprecation(
    "pythainlp.ulmfit",
    "pythainlp.lm.ulmfit",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "THWIKI_LSTM",
    "ThaiTokenizer",
    "document_vector",
    "fix_html",
    "get_thwiki_lstm",
    "lowercase_all",
    "merge_wgts",
    "post_rules_th",
    "post_rules_th_sparse",
    "pre_rules_th",
    "pre_rules_th_sparse",
    "process_thai",
    "remove_space",
    "replace_rep_after",
    "replace_rep_nonum",
    "replace_url",
    "replace_wrep_post",
    "replace_wrep_post_nonum",
    "rm_brackets",
    "rm_useless_newlines",
    "rm_useless_spaces",
    "spec_add_spaces",
    "ungroup_emoji",
]
