# -*- coding: utf-8 -*-
"""
Language translation.
"""

__all__ = [
    "EnThTranslator",
    "ThEnTranslator",
    "download_model_all",
    "ThZhTranslator",
    "ZhThTranslator",
    "Translate"
]

from pythainlp.translate.core import Translate

from pythainlp.translate.en_th import (
    EnThTranslator,
    ThEnTranslator,
    download_model_all,
)
from pythainlp.translate.zh_th import (
    ThZhTranslator,
    ZhThTranslator,
)
