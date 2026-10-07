# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Wrap the BudouX tokenizer.

This module provides a small, defensive wrapper around the Python
``budoux`` package (https://github.com/google/budoux).
The wrapper imports the package lazily, so importing
``pythainlp.tokenize`` does not fail if ``budoux`` is not installed.
When the wrapper is used and ``budoux`` is missing, it raises an
:class:`ImportError` with an installation hint.
"""

from __future__ import annotations

import threading
from typing import Any, Optional, cast

_parser: Optional[Any] = None
_parser_lock: threading.Lock = threading.Lock()


def _init_parser() -> Any:
    """
    Initialize a BudouX parser lazily and return it.

    :return: BudouX parser for Thai
    :rtype: typing.Any
    :raises ImportError: if ``budoux`` is not installed
    """
    try:
        import budoux
    except Exception as exc:  # pragma: no cover - defensive import
        raise ImportError(
            "budoux is not installed. Install it with: pip install budoux"
        ) from exc

    return budoux.load_default_thai_parser()


def segment(text: str) -> list[str]:
    """
    Tokenize text into words with BudouX.

    The wrapper uses a lock to protect lazy initialization of the parser.
    However, thread-safety of the underlying budoux library itself is not
    guaranteed. Refer to the budoux library documentation for its
    thread-safety guarantees.

    :param str text: text to be tokenized
    :return: list of words
    :rtype: list[str]
    :raises ImportError: if ``budoux`` is not installed
    :raises RuntimeError: if the parser fails to initialize
    """
    if not text or not isinstance(text, str):
        return []

    # Thread-safe lazy initialization
    global _parser
    with _parser_lock:
        if _parser is None:
            _parser = _init_parser()
        parser = _parser

    if parser is None:
        raise RuntimeError("Failed to initialize BudouX parser")

    result = cast("list[str]", parser.parse(text))

    return result
