# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
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
