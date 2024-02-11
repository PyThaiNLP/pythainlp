# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""

__all__ = [
    "soundex",
    "lk82",
    "metasound",
    "udom83",
    "prayut_and_somchaip",
]

from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.udom83 import udom83
from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip

DEFAULT_SOUNDEX_ENGINE = "udom83"

from pythainlp.soundex.core import soundex
