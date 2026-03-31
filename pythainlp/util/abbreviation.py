# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai abbreviation tools"""

from __future__ import annotations

from typing import Optional, cast


def abbreviation_to_full_text(
    text: str, top_k: int = 2
) -> list[tuple[str, Optional[float]]]:
    """Converts Thai text (with abbreviations) to full text.

    Uses KhamYo to handle abbreviations.
    See more: `KhamYo <https://github.com/wannaphong/KhamYo>`_.

    :param str text: Thai text
    :param int top_k: Top K
    :return: list of ``(full_text, cosine_similarity)`` tuples.
    :rtype: list[tuple[str, Optional[float]]]

    :Example:

        >>> from pythainlp.util import abbreviation_to_full_text  # doctest: +SKIP

        >>> text = "รร.ของเราน่าอยู่"  # doctest: +SKIP

        >>> abbreviation_to_full_text(text)  # doctest: +SKIP
        [
        ('โรงเรียนของเราน่าอยู่', tensor(0.3734)),
        ('โรงแรมของเราน่าอยู่', tensor(0.2438))
        ]
    """
    try:
        from khamyo import replace as _replace
    except ImportError as e:
        raise ImportError(
            "khamyo is required for this feature."
            " Install it with: pip install khamyo"
            " or pip install pythainlp[abbreviation]"
        ) from e
    return cast(list[tuple[str, Optional[float]]], _replace(text, top_k=top_k))
