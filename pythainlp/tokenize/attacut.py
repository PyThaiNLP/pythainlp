# -*- coding: utf-8 -*
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
Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai

:See Also:
    * `GitHub repository <https://github.com/PyThaiNLP/attacut>`_
"""
from typing import List

from attacut import Tokenizer


class AttacutTokenizer:
    def __init__(self, model="attacut-sc"):
        self._MODEL_NAME = "attacut-sc"

        if model == "attacut-c":
            self._MODEL_NAME = "attacut-c"

        self._tokenizer = Tokenizer(model=self._MODEL_NAME)

    def tokenize(self, text: str) -> List[str]:
        return self._tokenizer.tokenize(text)


def segment(text: str, model: str = "attacut-sc") -> List[str]:
    """
    Wrapper for AttaCut - Fast and Reasonably Accurate Word Tokenizer for Thai
    :param str text: text to be tokenized to words
    :param str model:  word tokenizer model to be tokenized to words
    :return: list of words, tokenized from the text
    :rtype: list[str]
    **Options for model**
        * *attacut-sc* (default) using both syllable and character features
        * *attacut-c* using only character feature
    """
    if not text or not isinstance(text, str):
        return []

    _tokenizer = AttacutTokenizer(model)

    return _tokenizer.tokenize(text)
