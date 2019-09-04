"""
Wrapper for deepcut Thai word segmentation. deepcut is a
Thai word segmentation library using Deep Neural, specifically,
1D Convolution Neural Network.
:See Also:
    * `GitHub repository <https://github.com/rkcosmos/deepcut>`_
"""

from typing import List, Union

import deepcut

from marisa_trie import Trie


def segment(text: str, custom_dict: Union[Trie, List[str], str] = None) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    if custom_dict:
        if isinstance(custom_dict, Trie):
            custom_dict = list(custom_dict)

        return deepcut.tokenize(text, custom_dict)

    return deepcut.tokenize(text)

