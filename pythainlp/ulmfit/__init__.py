# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
