# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Type stubs for pythainlp._ext._thai_fast Cython extension."""

def is_thai_char(ch: str) -> bool: ...
def is_thai(text: str, ignore_chars: str = ...) -> bool: ...
def count_thai(
    text: str,
    ignore_chars: str = ...,  # defaults to whitespace + digits + punctuation
) -> float: ...
