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
"""
Wrapper for PyICU word segmentation. This wrapper module uses
:class:`icu.BreakIterator` with Thai as :class:`icu.Local`
to locate boundaries between words from the text.

:See Also:
    * `GitHub repository <https://github.com/ovalhub/pyicu>`_
"""
import re
from typing import List

from icu import BreakIterator, Locale


def _gen_words(text: str) -> str:
    bd = BreakIterator.createWordInstance(Locale("th"))
    bd.setText(text)
    p = bd.first()
    for q in bd:
        yield text[p:q]
        p = q


def segment(text: str) -> List[str]:
    """
    :param str text: text to be tokenized to words
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    text = re.sub("([^\u0E00-\u0E7F\n ]+)", " \\1 ", text)

    return list(_gen_words(text))
