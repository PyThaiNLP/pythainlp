# -*- coding: utf-8 -*-
"""
Utility functions for tokenize module.
"""

import re
from typing import List, Callable

_DIGITS_WITH_SEPARATOR = re.compile(r"(\d+(\.|\,|:))+\d+")


def postprocess_word_tokenize(segments: List[str]) -> List[str]:
    """
    A list of callables to apply on a raw word segmentation result.
    """
    post_processors: Callable[[List[str]], List[str]] = [
        _fix_broken_numeric_data_format
    ]

    for func in post_processors:
        segments = func(segments)

    return segments


def _fix_broken_numeric_data_format(segments: List[str]) -> List[str]:
    """
    Fix well-known numeric formats that are over-tokenized.
    The numeric formats are numbers separated by either ":", ",", or ".".
    such as time, decimal number, comma-added number, and IP address.

    :param List[str] segments: result from word tokenizer
    :return: a list of fixed tokens
    :rtype: List[str]

    :Example:
        text = ['ขณะ', 'นี้', 'เวลา', ' ', '12', ':', '00น', ' ', 'อัตรา',
                'แลกเปลี่ยน', ' ', '1', ',', '234', '.', '5', ' ', 'baht/zeny']
        _fix_broken_digits(text)
        # output:
        # ['ขณะ', 'นี้', 'เวลา', ' ', '12:00น', ' ', 'อัตรา', 'แลกเปลี่ยน', ' ', '1,234.5', ' ', 'baht/zeny']

        text = ['IP', ' ', 'address', ' ', 'ของ', 'คุณ', 'คือ', ' ', '127', '.', '0', '.', '0', '.', '1', ' ', 'ครับ']
        _fix_broken_digits(text)
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
