# -*- coding: utf-8 -*-
"""
Text summarization
"""

__all__ = [
    "summarize",
]

DEFAULT_SUMMARIZE_ENGINE = "frequency"

from pythainlp.summarize.core import summarize
