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
Wrapper OSKut (Out-of-domain StacKed cut for Word Segmentation).
Handling Cross- and Out-of-Domain Samples in Thai Word Segmentation
Stacked Ensemble Framework and DeepCut as Baseline model (ACL 2021 Findings)

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/OSKut>`_
"""
from typing import List

import oskut

DEFAULT_ENGINE = "ws"
oskut.load_model(engine=DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws") -> List[str]:
    global DEFAULT_ENGINE
    if not text or not isinstance(text, str):
        return []
    if engine != DEFAULT_ENGINE:
        DEFAULT_ENGINE = engine
        oskut.load_model(engine=DEFAULT_ENGINE)
    return oskut.OSKut(text)
