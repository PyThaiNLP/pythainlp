# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Performance benchmarking."""

__all__: list[str] = ["benchmark", "bleu_score", "rouge_score"]

from pythainlp.benchmarks.metrics import bleu_score, rouge_score
from pythainlp.benchmarks.word_tokenization import benchmark
