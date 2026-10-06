# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Utility functions for the tokenize module."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

_DIGITS_WITH_SEPARATOR: re.Pattern[str] = re.compile(r"(\d+[\.\,:])+\d+")


def apply_postprocessors(
    segments: list[str],
    postprocessors: Sequence[Callable[[list[str]], list[str]]],
) -> list[str]:
    """
    Apply postprocessors, in order, to a raw tokenization result.

    :param list[str] segments: raw result from a word tokenizer
    :param Sequence[Callable[[list[str]], list[str]]] postprocessors:
        callables to apply, each taking and returning a list of words
    :return: list of words after all postprocessors
    :rtype: list[str]
    """
    for func in postprocessors:
        segments = func(segments)

    return segments


def rejoin_formatted_num(segments: list[str]) -> list[str]:
    """
    Rejoin formatted numbers that a tokenizer split into several words.

    Formatted numbers are numbers separated by ":", ",", or ".",
    such as times, decimal numbers, comma-separated numbers, and
    IP addresses.

    :param list[str] segments: result from a word tokenizer
    :return: list of words with formatted numbers rejoined
    :rtype: list[str]

    :Example:

        >>> from pythainlp.tokenize._utils import rejoin_formatted_num
        >>> tokens = [
        ...     "ขณะ",
        ...     "นี้",
        ...     "เวลา",
        ...     " ",
        ...     "12",
        ...     ":",
        ...     "00น",
        ...     " ",
        ...     "อัตรา",
        ...     "แลกเปลี่ยน",
        ...     " ",
        ...     "1",
        ...     ",",
        ...     "234",
        ...     ".",
        ...     "5",
        ...     " ",
        ...     "baht/zeny",
        ... ]
        >>> rejoin_formatted_num(tokens)
        ['ขณะ', 'นี้', 'เวลา', ' ', '12:00น', ' ', 'อัตรา', 'แลกเปลี่ยน', ' ', '1,234.5', ' ', 'baht/zeny']
        >>> tokens = [
        ...     "IP",
        ...     " ",
        ...     "address",
        ...     " ",
        ...     "ของ",
        ...     "คุณ",
        ...     "คือ",
        ...     " ",
        ...     "127",
        ...     ".",
        ...     "0",
        ...     ".",
        ...     "0",
        ...     ".",
        ...     "1",
        ...     " ",
        ...     "ครับ",
        ... ]
        >>> rejoin_formatted_num(tokens)
        ['IP', ' ', 'address', ' ', 'ของ', 'คุณ', 'คือ', ' ', '127.0.0.1', ' ', 'ครับ']
    """
    original = "".join(segments)
    matching_results = _DIGITS_WITH_SEPARATOR.finditer(original)
    tokens_joined = []
    pos = 0
    segment_idx = 0

    match = next(matching_results, None)
    while segment_idx < len(segments) and match:
        is_span_beginning = pos >= match.start()
        token = segments[segment_idx]
        if is_span_beginning:
            connected_token = ""  # nosec B105
            while pos < match.end() and segment_idx < len(segments):
                connected_token += segments[segment_idx]
                pos += len(segments[segment_idx])
                segment_idx += 1
            if connected_token:
                tokens_joined.append(connected_token)
            match = next(matching_results, None)
        else:
            tokens_joined.append(token)
            segment_idx += 1
            pos += len(token)
    tokens_joined += segments[segment_idx:]
    return tokens_joined


def strip_whitespace(segments: list[str]) -> list[str]:
    """
    Strip whitespace from each word and remove whitespace-only words.

    :param list[str] segments: result from a word tokenizer
    :return: list of words without whitespace
    :rtype: list[str]

    :Example:

        >>> from pythainlp.tokenize._utils import strip_whitespace
        >>> tokens = [" ", "วันนี้ ", "เวลา ", "19.00น"]
        >>> strip_whitespace(tokens)
        ['วันนี้', 'เวลา', '19.00น']

    """
    segments = [token.strip(" ") for token in segments if token.strip(" ")]
    return segments
