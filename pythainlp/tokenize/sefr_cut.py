# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Wrapper for SEFR CUT Thai word segmentation. SEFR CUT is a
Thai Word Segmentation Models using Stacked Ensemble.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/SEFR_CUT>`_
"""
from typing import List

import sefr_cut

DEFAULT_ENGINE = "ws1000"
sefr_cut.load_model(engine=DEFAULT_ENGINE)


def segment(text: str, engine: str = "ws1000") -> List[str]:
    global DEFAULT_ENGINE
    if not text or not isinstance(text, str):
        return []
    if engine != DEFAULT_ENGINE:
        DEFAULT_ENGINE = engine
        sefr_cut.load_model(engine=DEFAULT_ENGINE)
    return sefr_cut.tokenize(text)[0]
