# -*- coding: utf-8 -*-
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
from pythainlp.ulmfit.tokenizer import ThaiTokenizer
