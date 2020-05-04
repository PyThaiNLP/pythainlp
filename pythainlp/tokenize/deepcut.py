# -*- coding: utf-8 -*-
"""
Wrapper for deepcut Thai word segmentation. deepcut is a
Thai word segmentation library using 1D Convolution Neural Network.

User need to install deepcut (and its dependency: tensorflow) by themselves.

:See Also:
    * `GitHub repository <https://github.com/rkcosmos/deepcut>`_
"""

from typing import List, Union

from deepcut import tokenize
from pythainlp.util import Trie


def segment(
    text: str, custom_dict: Union[Trie, List[str], str] = None
) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    if custom_dict:
        if isinstance(custom_dict, Trie):
            custom_dict = list(custom_dict)

        return tokenize(text, custom_dict)

    return tokenize(text)
