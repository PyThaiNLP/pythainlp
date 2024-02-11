# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Universal Language Model Fine-tuning for Text Classification (ULMFiT).

Code by Charin Polpanumas
https://github.com/cstorm125/thai2fit/

Some pre-processing functions are from fastai (Apache 2.0)
https://github.com/fastai/fastai/blob/master/fastai/text/transform.py

Universal Language Model Fine-tuning for Text Classification
https://arxiv.org/abs/1801.06146
"""

__all__ = [
    "THWIKI_LSTM",
    "ThaiTokenizer",
    "document_vector",
    "merge_wgts",
    "post_rules_th",
    "post_rules_th_sparse",
    "pre_rules_th",
    "pre_rules_th_sparse",
    "process_thai",
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

from pythainlp.ulmfit.core import (
    THWIKI_LSTM,
    document_vector,
    merge_wgts,
    post_rules_th,
    post_rules_th_sparse,
    pre_rules_th,
    pre_rules_th_sparse,
    process_thai,
)
from pythainlp.ulmfit.preprocess import (
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
from pythainlp.ulmfit.tokenizer import ThaiTokenizer
