# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from pythainlp.tools import warn_deprecation


def is_native_thai(word: str) -> bool:
    warn_deprecation(
        "pythainlp.util.is_native_thai",
        "pythainlp.morpheme.is_native_thai",
        "5.0",
        "5.1",
    )

    from pythainlp.morpheme import is_native_thai as check

    return check(word)
