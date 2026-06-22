# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Transliteration."""

__all__: list[str] = [
    "get_word_dict",
    "pronunciate",
    "puan",
    "romanize",
    "th_pron_transliterate",
    "transliterate",
]

from pythainlp.transliterate.core import pronunciate, romanize, transliterate
from pythainlp.transliterate.spoonerism import puan
from pythainlp.transliterate.th_pron import (
    get_word_dict,
    th_pron_transliterate,
)
