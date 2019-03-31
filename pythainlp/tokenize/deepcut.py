# -*- coding: utf-8 -*-
"""
Wrapper for deepcut Thai word segmentation
"""

import deepcut


def segment(text):
    return deepcut.tokenize(text)
