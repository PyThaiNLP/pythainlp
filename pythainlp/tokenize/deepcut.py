# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for deepcut Thai word segmentation. deepcut is a
Thai word segmentation library using 1D Convolution Neural Network.

User need to install deepcut (and its dependency: tensorflow) by themselves.

:See Also:
    * `GitHub repository <https://github.com/rkcosmos/deepcut>`_
"""

from __future__ import annotations

from typing import Union, cast

try:
    from deepcut import tokenize
except ImportError as e:
    raise ImportError(
        "deepcut is not installed. Install it with: pip install deepcut"
    ) from e
from pythainlp.util import Trie


def segment(
    text: str, custom_dict: Union[Trie, list[str], str] = []
) -> list[str]:
    if not text or not isinstance(text, str):
        return []

    if custom_dict:
        if isinstance(custom_dict, Trie):
            custom_dict = list(custom_dict)

        return cast("list[str]", tokenize(text, custom_dict))

    return cast("list[str]", tokenize(text))
