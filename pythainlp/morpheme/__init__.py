# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""PyThaiNLP morpheme"""

__all__: list[str] = ["nighit", "is_native_thai"]
from pythainlp.morpheme.thaiwordcheck import is_native_thai
from pythainlp.morpheme.word_formation import nighit
