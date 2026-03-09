# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import cast

from ssg import syllable_tokenize


def segment(text: str) -> list[str]:
    """Syllable tokenizer using ssg"""
    if not text or not isinstance(text, str):
        return []

    return cast("list[str]", syllable_tokenize(text))
