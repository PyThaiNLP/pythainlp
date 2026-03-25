# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Performance benchmarking."""

__all__: list[str] = [
    "BleuScore",
    "CharLevelStat",
    "GlobalStat",
    "RougeScore",
    "TokenizationStat",
    "WordLevelStat",
    "benchmark",
    "bleu_score",
    "character_error_rate",
    "rouge_score",
    "word_error_rate",
]

from pythainlp.benchmarks.metrics import (
    BleuScore,
    RougeScore,
    bleu_score,
    character_error_rate,
    rouge_score,
    word_error_rate,
)
from pythainlp.benchmarks.word_tokenization import (
    CharLevelStat,
    GlobalStat,
    TokenizationStat,
    WordLevelStat,
    benchmark,
)
