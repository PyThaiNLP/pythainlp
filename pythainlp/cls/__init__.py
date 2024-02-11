# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
pythainlp.cls
Depreciated. Use pythainlp.classify instead.
"""
import warnings

__all__ = ["GzipModel"]

from pythainlp.classify.param_free import GzipModel

warnings.warn(
    "Deprecated: Use pythainlp.classify instead.", DeprecationWarning
)
