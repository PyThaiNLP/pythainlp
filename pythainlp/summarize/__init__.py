# -*- coding: utf-8 -*-
"""
Text summarization
"""

__all__ = [
    "summarize",
    "extract_keywords"
]

DEFAULT_SUMMARIZE_ENGINE = "frequency"
CPE_KMUTT_THAI_SENTENCE_SUM = "mt5-cpe-kmutt-thai-sentence-sum"
DEFAULT_KEYWORD_EXTRACTION_ENGINE = "keybert"

from pythainlp.summarize.core import summarize, extract_keywords
