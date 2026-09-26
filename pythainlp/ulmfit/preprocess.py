# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :mod:`pythainlp.lm.ulmfit.preprocess` instead.

.. deprecated:: 5.3.9
    :mod:`pythainlp.ulmfit.preprocess` has moved to :mod:`pythainlp.lm.ulmfit.preprocess`.
"""

from __future__ import annotations

from pythainlp.lm.ulmfit.preprocess import (
    fix_html,
    lowercase_all,
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
    "pythainlp.ulmfit.preprocess",
    "pythainlp.lm.ulmfit.preprocess",
    "5.3.9",
    "6.0",
)

__all__: list[str] = [
    "fix_html",
    "lowercase_all",
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
