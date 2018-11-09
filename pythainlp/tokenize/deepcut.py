# -*- coding: utf-8 -*-
"""
Wrapper for deepcut Thai word segmentation
"""

import deepcut


def segment(text):
    if not text:
        return []

    return deepcut.tokenize(text)
