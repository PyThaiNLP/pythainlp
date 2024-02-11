# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
TLTK

Thai Language Toolkit

:See Also:
    * \
        https://pypi.org/project/tltk/
"""
try:
    from tltk.nlp import spell_candidates
except ImportError:
    raise ImportError("Not found tltk! Please install tltk by pip install tltk")
from typing import List


def spell(text: str) -> List[str]:
    return spell_candidates(text)
