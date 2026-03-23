# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Wrapper for BudouX tokenizer (https://github.com/google/budoux)

This module provides a small, defensive wrapper around the Python
`budoux` package. The wrapper lazy-imports the package so importing
`pythainlp.tokenize` will not fail if `budoux` is not installed. When
used and `budoux` is missing, a clear ImportError is raised with an
installation hint.
"""

from __future__ import annotations

import threading
from typing import Any, Optional, cast

_parser: Optional[Any] = None
_parser_lock: threading.Lock = threading.Lock()


def _init_parser() -> Any:
    """Lazy initialize and return a budoux parser instance.

    Raises ImportError when `budoux` is not installed, and RuntimeError
    if the installed budoux does not expose a supported API.
    """
    try:
        import budoux
    except Exception as exc:  # pragma: no cover - defensive import
        raise ImportError(
            "budoux is not installed. Install it with: pip install budoux"
        ) from exc

    return budoux.load_default_thai_parser()


def segment(text: str) -> list[str]:
    """Segment `text` into tokens using budoux.

    The wrapper uses a lock to protect lazy initialization of the parser.
    However, thread-safety of the underlying budoux library itself is not
    guaranteed. Please refer to the budoux library documentation for its
    thread-safety guarantees.

    The function returns a list of strings. If `budoux` is not available
    the function raises ImportError with an installation hint.
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
