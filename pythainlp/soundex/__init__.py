# -*- coding: utf-8 -*-
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""

__all__ = [
    "soundex",
    "lk82",
    "metasound",
    "udom83",
]

from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.udom83 import udom83

DEFAULT_SOUNDEX_ENGINE = "udom83"

from pythainlp.soundex.core import soundex
