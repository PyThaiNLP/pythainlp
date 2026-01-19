# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

__all__ = ["calculate_ngram_counts", "remove_repeated_ngrams", "Qwen3"]

from pythainlp.lm.text_util import (
    calculate_ngram_counts,
    remove_repeated_ngrams,
)

try:
    from pythainlp.lm.qwen3 import Qwen3
except ImportError:
    # If dependencies are not installed, make Qwen3 available but raise
    # error when instantiated
    class Qwen3:  # type: ignore
        def __init__(self):
            raise ImportError(
                "Qwen3 requires additional dependencies. "
                "Install with: pip install pythainlp[qwen3]"
            )
