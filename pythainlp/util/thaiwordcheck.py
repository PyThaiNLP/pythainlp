# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
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
