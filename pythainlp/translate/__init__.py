# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Language translation."""

__all__: list[str] = [
    "Translate",
    "ThZhTranslator",
    "ZhThTranslator",
    "word_translate",
]

from pythainlp.translate.core import Translate, word_translate
from pythainlp.translate.zh_th import (
    ThZhTranslator,
    ZhThTranslator,
)
