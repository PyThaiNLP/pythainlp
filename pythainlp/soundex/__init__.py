# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""

__all__ = [
    "complete_soundex",
    "lk82",
    "metasound",
    "prayut_and_somchaip",
    "soundex",
    "udom83",
]

from pythainlp.soundex.complete_soundex import complete_soundex
from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip
from pythainlp.soundex.udom83 import udom83

DEFAULT_SOUNDEX_ENGINE = "udom83"

from pythainlp.soundex.core import soundex
