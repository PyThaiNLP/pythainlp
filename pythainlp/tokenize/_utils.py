# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Utility functions for tokenize module.
"""

import re
from typing import List, Callable

_DIGITS_WITH_SEPARATOR = re.compile(r"(\d+[\.\,:])+\d+")


def apply_postprocessors(
    segments: List[str], postprocessors: Callable[[List[str]], List[str]]
) -> List[str]:
    """
    A list of callables to apply to a raw segmentation result.
    """
    for func in postprocessors:
        segments = func(segments)

    return segments


def rejoin_formatted_num(segments: List[str]) -> List[str]:
    """
    Rejoin well-known formatted numeric that are over-tokenized.
    The formatted numeric are numbers separated by ":", ",", or ".",
    such as time, decimal numbers, comma-added numbers, and IP addresses.

    :param List[str] segments: result from word tokenizer
    :return: a list of fixed tokens
    :rtype: List[str]

    :Example:
        tokens = ['ขณะ', 'นี้', 'เวลา', ' ', '12', ':', '00น', ' ', 'อัตรา',
                'แลกเปลี่ยน', ' ', '1', ',', '234', '.', '5', ' ', 'baht/zeny']
        rejoin_formatted_num(tokens)
        # output:
        # ['ขณะ', 'นี้', 'เวลา', ' ', '12:00น', ' ', 'อัตรา', 'แลกเปลี่ยน', ' ', '1,234.5', ' ', 'baht/zeny']

        tokens = ['IP', ' ', 'address', ' ', 'ของ', 'คุณ', 'คือ', ' ', '127', '.', '0', '.', '0', '.', '1', ' ', 'ครับ']
        rejoin_formatted_num(tokens)
        # output:
        # ['IP', ' ', 'address', ' ', 'ของ', 'คุณ', 'คือ', ' ', '127.0.0.1', ' ', 'ครับ']
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
            connected_token = ""
            while pos < match.end() and segment_idx < len(segments):
                connected_token += segments[segment_idx]
                pos += len(segments[segment_idx])
                segment_idx += 1

            tokens_joined.append(connected_token)
            match = next(matching_results, None)
        else:
            tokens_joined.append(token)
            segment_idx += 1
            pos += len(token)
    tokens_joined += segments[segment_idx:]
    return tokens_joined


def strip_whitespace(segments: List[str]) -> List[str]:
    """
    Strip whitespace(s) off each token and remove whitespace tokens.
    :param List[str] segments: result from word tokenizer
    :return: a list of tokens
    :rtype: List[str]

    :Example:
        tokens = [" ", "วันนี้ ", "เวลา ", "19.00น"]
        strip_whitespace(tokens)
        # ["วันนี้", "เวลา", "19.00น"]

    """
    segments = [token.strip(" ") for token in segments if token.strip(" ")]
    return segments
