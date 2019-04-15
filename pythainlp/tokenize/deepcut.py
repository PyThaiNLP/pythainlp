# -*- coding: utf-8 -*-
"""
Wrapper for deepcut Thai word segmentation
"""

from typing import List

import deepcut


def segment(text: str,dict_source:List[str]=None) -> List[str]:
    if dict_source!=None:
        return deepcut.tokenize(text, custom_dict=dict_source)
    return deepcut.tokenize(text)
