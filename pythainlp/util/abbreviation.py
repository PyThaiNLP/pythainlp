# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai abbreviation tools
"""

from __future__ import annotations


def abbreviation_to_full_text(
    text: str, top_k: int = 2
) -> list[tuple[str, float | None]]:
    """
    This function converts Thai text (with abbreviation) to full text.

    This function uses KhamYo for handles abbreviations.
    See more `KhamYo <https://github.com/wannaphong/KhamYo>`_.

    :param str text: Thai text
    :param int top_k: Top K
    :return: Thai full text with abbreviations converted to full text and cos scores (original text - modified text).
    :rtype: List[Tuple[str, Union[float, None]]]

    :Example:
    ::

        from pythainlp.util import abbreviation_to_full_text

        text = "รร.ของเราน่าอยู่"

        abbreviation_to_full_text(text)
        # output: [
        # ('โรงเรียนของเราน่าอยู่', tensor(0.3734)),
        # ('โรงแรมของเราน่าอยู่', tensor(0.2438))
        # ]
    """
    try:
        from khamyo import replace as _replace
    except ImportError:
        raise ImportError(
            """
            This function needs to use khamyo.
            You can install by pip install khamyo or
            pip install pythainlp[abbreviation].
            """
        )
    return _replace(text, top_k=top_k)
