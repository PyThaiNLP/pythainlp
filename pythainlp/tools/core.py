# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Generic support functions for PyThaiNLP."""

from __future__ import annotations

import sys
import warnings


def warn_deprecation(
    deprecated_symbol: str,
    replacing_symbol: str = "",
    deprecated_version: str = "",
    removal_version: str = "",
) -> None:
    """Warn about the deprecation of a function, class, or other symbol.

    :param str deprecated_symbol: Fully qualified name of the deprecated
        symbol (e.g. ``"pythainlp.util.isthaichar"``).
    :param str replacing_symbol: Fully qualified name of the replacement
        (optional).
    :param str deprecated_version: Version in which the symbol was
        deprecated (optional).
    :param str removal_version: Version in which the symbol will be
        removed (optional).
    """
    message = f"'{deprecated_symbol}' is deprecated"
    if deprecated_version:
        message += f" since {deprecated_version}"
    if not removal_version:
        removal_version = "a future release"
    message += f" and will be removed in {removal_version}."
    if replacing_symbol:
        message += f" Use '{replacing_symbol}' instead."
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def safe_print(text: str) -> None:
    """Print text to console, handling UnicodeEncodeError.

    :param text: Text to print.
    :type text: str
    """
    try:
        print(text)
    except UnicodeEncodeError:
        print(
            text.encode(sys.stdout.encoding, errors="replace").decode(
                sys.stdout.encoding
            )
        )
