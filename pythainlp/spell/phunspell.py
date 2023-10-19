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
Phunspell

A pure Python spell checker utilizing spylls, a port of Hunspell.

:See Also:
    * \
        https://github.com/dvwright/phunspell
"""
from typing import List
import phunspell

pspell = phunspell.Phunspell("th_TH")


def spell(text: str) -> List[str]:
    return list(pspell.suggest(text))


def correct(text: str) -> str:
    return list(pspell.suggest(text))[0]
