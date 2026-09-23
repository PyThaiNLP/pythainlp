# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Performance benchmarking."""

__all__: list[str] = [
    "BleuScore",
    "CharLevelStat",
    "GlobalStat",
    "RougeScore",
    "TokenizationScore",
    "TokenizationStat",
    "WordLevelStat",
    "benchmark",
    "bleu_score",
    "char_eval_function",
    "character_error_rate",
    "evaluate_word_tokenization",
    "rouge_score",
    "word_error_rate",
    "word_eval_function",
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
    TokenizationScore,
    TokenizationStat,
    WordLevelStat,
    benchmark,
    char_eval_function,
    evaluate_word_tokenization,
    word_eval_function,
)
