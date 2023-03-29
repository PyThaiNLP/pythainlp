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
Transliterating text to International Phonetic Alphabet (IPA)
Using epitran

:See Also:
    * `GitHub \
        <https://github.com/dmort27/epitran>`_
"""
from typing import List

import epitran

_EPI_THA = epitran.Epitran("tha-Thai")


def transliterate(text: str) -> str:
    return _EPI_THA.transliterate(text)


def trans_list(text: str) -> List[str]:
    return _EPI_THA.trans_list(text)


def xsampa_list(text: str) -> List[str]:
    return _EPI_THA.xsampa_list(text)
