# -*- coding: utf-8 -*-
"""
Text summarization
"""

__all__ = [
    "summarize",
]

DEFAULT_SUMMARIZE_ENGINE = "frequency"
CPE_KMUTT_THAI_SENTENCE_SUM = "mt5-cpe-kmutt-thai-sentence-sum"

from pythainlp.summarize.core import summarize
