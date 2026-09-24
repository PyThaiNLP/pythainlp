# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Transliteration."""

__all__: list[str] = [
    "FastThaiG2P",
    "get_word_dict",
    "pronunciate",
    "puan",
    "romanize",
    "transliterate",
    "transliterate_wiktionary",
    "pronunciate_pali",
]

from pythainlp.transliterate.core import pronunciate, romanize, transliterate
from pythainlp.transliterate.fastthaig2p import FastThaiG2P
from pythainlp.transliterate.pali import pronunciate_pali
from pythainlp.transliterate.spoonerism import puan
from pythainlp.transliterate.wiktionary import (
    get_word_dict,
    transliterate_wiktionary,
)
