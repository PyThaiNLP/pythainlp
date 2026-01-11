# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text summarization
"""

__all__ = [
    "extract_keywords",
    "summarize",
]

DEFAULT_SUMMARIZE_ENGINE = "frequency"
CPE_KMUTT_THAI_SENTENCE_SUM = "mt5-cpe-kmutt-thai-sentence-sum"
DEFAULT_KEYWORD_EXTRACTION_ENGINE = "keybert"

# these imports are placed here to avoid circular imports
from pythainlp.summarize.core import extract_keywords, summarize
