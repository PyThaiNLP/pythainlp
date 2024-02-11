# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import warnings

def is_native_thai(word: str) -> bool:
    warnings.warn(
        """
        pythainlp.util.is_native_thai is rename as \
            pythainlp.morpheme.is_native_thai.
        This function will remove in PyThaiNLP 5.1.
        """, DeprecationWarning)
    from pythainlp.morpheme import is_native_thai as check

    return check(word)
