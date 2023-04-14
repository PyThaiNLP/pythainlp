# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
