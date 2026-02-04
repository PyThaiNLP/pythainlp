# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Text summarization"""

__all__: list[str] = [
    "extract_keywords",
    "summarize",
]

DEFAULT_SUMMARIZE_ENGINE: str = "frequency"
CPE_KMUTT_THAI_SENTENCE_SUM: str = "mt5-cpe-kmutt-thai-sentence-sum"
DEFAULT_KEYWORD_EXTRACTION_ENGINE: str = "keybert"

# these imports are placed here to avoid circular imports
from pythainlp.summarize.core import extract_keywords, summarize
