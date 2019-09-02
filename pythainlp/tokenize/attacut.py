"""
Wrapper for AttaCut - a resonable fast thai word segmentation
:See Also:
    * `GitHub repository <https://github.com/rkcosmos/deepcut>`_
"""
from typing import List, Union

import attacut


def segment(text: str):
    if not text or not isinstance(text, str):
        return []
        
    return attacut.tokenize(text)
