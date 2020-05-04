# -*- coding: utf-8 -*-
"""
Text summarization
"""

__all__ = [
    "summarize",
]

DEFAULT_SUMMARIZE_ENGINE = "freq"

from pythainlp.summarize.core import summarize
