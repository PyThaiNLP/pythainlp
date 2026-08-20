# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Type stubs for pythainlp._ext._normalize_fast Cython extension."""

def remove_tonemark(text: str) -> str: ...
def remove_dup_spaces(text: str) -> str: ...
