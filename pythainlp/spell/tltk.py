# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
TLTK

Thai Language Toolkit

:See Also:
    * \
        https://pypi.org/project/tltk/
"""

from __future__ import annotations

try:
    from tltk.nlp import spell_candidates
except ImportError:
    raise ImportError(
        "Not found tltk! Please install tltk by pip install tltk"
    )


def spell(text: str) -> list[str]:
    return spell_candidates(text)
