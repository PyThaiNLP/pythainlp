# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Location tagger."""

from __future__ import annotations

from pythainlp.corpus import provinces


def tag_provinces(tokens: list[str]) -> list[tuple[str, str]]:
    """
    Tag Thailand provinces in text.

    This function uses exact match and considers no context.

    :param list[str] tokens: list of words to be tagged
    :return: list of tuples (word, IOB tag), where the tag is
        ``B-LOCATION`` for a province and ``O`` otherwise
    :rtype: list[tuple[str, str]]

    :Example:

        >>> from pythainlp.tag import tag_provinces  # doctest: +SKIP

        >>> text = ["หนองคาย", "น่าอยู่"]  # doctest: +SKIP
        >>> tag_provinces(text)  # doctest: +SKIP
        [('หนองคาย', 'B-LOCATION'), ('น่าอยู่', 'O')]
    """
    province_list = provinces()
    output = [
        (token, "B-LOCATION") if token in province_list else (token, "O")
        for token in tokens
    ]
    return output
