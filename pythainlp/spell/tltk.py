# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""TLTK

Thai Language Toolkit

:See Also:
    * \
        https://pypi.org/project/tltk/
"""

from __future__ import annotations

from typing import cast

try:
    from tltk.nlp import spell_candidates
except ImportError as e:
    raise ImportError(
        "tltk is not installed. Install it with: pip install tltk"
    ) from e


def spell(text: str) -> list[str]:
    return cast(list[str], spell_candidates(text))
