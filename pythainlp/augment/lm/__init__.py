# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2016-2023 PyThaiNLP Project.
# SPDX-License-Identifier: Apache-2.0
"""
LM
"""

__all__ = [
    "FastTextAug",
    "Thai2transformersAug",
]

from pythainlp.augment.lm.fasttext import FastTextAug
from pythainlp.augment.lm.wangchanberta import Thai2transformersAug
