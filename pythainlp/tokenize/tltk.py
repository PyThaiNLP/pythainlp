# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

try:
    from tltk.nlp import syl_segment
    from tltk.nlp import word_segment as tltk_segment
except ImportError:
    raise ImportError(
        "Not found tltk! Please install tltk by pip install tltk"
    )


def segment(text: str) -> list[str]:
    if not text or not isinstance(text, str):
        return []
    text = text.replace(" ", "<u/>")
    _temp: str = tltk_segment(text).replace("<u/>", " ").replace("<s/>", "")
    _temp_list = _temp.split("|")
    if _temp_list[-1] == "":
        del _temp_list[-1]
    return _temp_list


def syllable_tokenize(text: str) -> list[str]:
    if not text or not isinstance(text, str):
        return []
    _temp: str = syl_segment(text)
    _temp_list = _temp.split("~")
    if _temp_list[-1] == "<s/>":
        del _temp_list[-1]
    return _temp_list


def sent_tokenize(text: str) -> list[str]:
    text = text.replace(" ", "<u/>")
    _temp: str = tltk_segment(text).replace("<u/>", " ").replace("|", "")
    _temp_list = _temp.split("<s/>")
    if _temp_list[-1] == "":
        del _temp_list[-1]
    return _temp_list
