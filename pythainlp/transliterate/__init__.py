# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Transliteration.
"""

__all__ = ["romanize", "transliterate", "pronunciate", "puan"]

from pythainlp.transliterate.core import romanize, transliterate, pronunciate
from pythainlp.transliterate.spoonerism import puan
