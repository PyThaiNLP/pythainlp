# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from typing import List
try:
    from tltk.nlp import word_segment as tltk_segment
    from tltk.nlp import syl_segment
except ImportError:
    raise ImportError("Not found tltk! Please install tltk by pip install tltk")


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []
    text = text.replace(" ", "<u/>")
    _temp = tltk_segment(text).replace("<u/>", " ").replace("<s/>", "")
    _temp = _temp.split("|")
    if _temp[-1] == "":
        del _temp[-1]
    return _temp


def syllable_tokenize(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []
    _temp = syl_segment(text)
    _temp = _temp.split("~")
    if _temp[-1] == "<s/>":
        del _temp[-1]
    return _temp


def sent_tokenize(text: str) -> List[str]:
    text = text.replace(" ", "<u/>")
    _temp = tltk_segment(text).replace("<u/>", " ").replace("|", "")
    _temp = _temp.split("<s/>")
    if _temp[-1] == "":
        del _temp[-1]
    return _temp
