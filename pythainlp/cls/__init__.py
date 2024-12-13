# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
pythainlp.cls
Depreciated. Use pythainlp.classify instead.
"""

__all__ = ["GzipModel"]

from pythainlp.classify.param_free import GzipModel
from pythainlp.tools import warn_deprecation

warn_deprecation("pythainlp.cls", "pythainlp.classify", "5.1", "5.2")
