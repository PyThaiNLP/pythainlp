# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Text summarization
"""

__all__ = ["summarize", "extract_keywords"]

DEFAULT_SUMMARIZE_ENGINE = "frequency"
CPE_KMUTT_THAI_SENTENCE_SUM = "mt5-cpe-kmutt-thai-sentence-sum"
DEFAULT_KEYWORD_EXTRACTION_ENGINE = "keybert"

from pythainlp.summarize.core import summarize, extract_keywords
