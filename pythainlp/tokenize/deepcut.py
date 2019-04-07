# -*- coding: utf-8 -*-
"""
Wrapper for deepcut Thai word segmentation
"""

from typing import List

import deepcut


def segment(text: str) -> List[str]:
    return deepcut.tokenize(text)
