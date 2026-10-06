# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrap ssg, a syllable tokenizer for Thai."""

from __future__ import annotations

from typing import cast

from ssg import syllable_tokenize


def segment(text: str) -> list[str]:
    """
    Tokenize text into syllables with ssg.

    :param str text: text to be tokenized
    :return: list of syllables
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    return cast("list[str]", syllable_tokenize(text))
