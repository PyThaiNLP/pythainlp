# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Cycle detection for greedy seq2seq decoding.

Greedy decoding (picking the highest-probability token at each step,
with no repetition penalty or n-gram blocking) can get the decoder
stuck in a loop: the attention mechanism repeatedly attends to the
same input position and keeps emitting the same short token sequence
until the hard length limit is hit. This module detects such a cycle
as it forms so a caller can stop decoding early instead of returning
an unbounded run of repeated characters.

See: https://github.com/PyThaiNLP/pythainlp/issues/1403
"""

from __future__ import annotations

from typing import List, Optional

__all__: List[str] = ["find_trailing_repeat_period"]


def find_trailing_repeat_period(
    tokens: List[int],
    min_period: int = 1,
    max_period: int = 12,
    min_repeats: int = 3,
) -> Optional[int]:
    """Detect a short cycle repeating at the end of a token sequence.

    Checks period lengths from ``min_period`` to ``max_period``
    (smallest first) and returns the first period whose last
    ``min_repeats`` copies at the end of ``tokens`` are identical.

    :param tokens: sequence of decoded token ids, in generation order
    :param min_period: shortest cycle length to check, in tokens
    :param max_period: longest cycle length to check, in tokens
    :param min_repeats: number of consecutive copies of the cycle
        required at the end of ``tokens`` to count as a repetition loop
    :return: the period of the detected cycle, or None if no trailing
        cycle of at least ``min_repeats`` copies is found
    :rtype: Optional[int]
    """
    n = len(tokens)
    for period in range(min_period, max_period + 1):
        window = period * min_repeats
        if n < window:
            continue
        segment = tokens[-window:]
        first = segment[:period]
        if all(
            segment[i * period : (i + 1) * period] == first
            for i in range(1, min_repeats)
        ):
            return period
    return None
