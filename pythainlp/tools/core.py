# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Generic support functions for PyThaiNLP.
"""

import sys
import warnings


def warn_deprecation(
    deprecated_func: str,
    replacing_func: str = "",
    deprecated_version: str = "",
    removal_version: str = "",
):
    """Warn about the deprecation of a function.

    :param str deprecated_func: Name of the deprecated function.
    :param str replacing_func: Name of the function to use instead (optional).
    :param str deprecated_version: Version in which the function will be deprecated (optional).
    :param str removal_version: Version in which the function will be removed (optional).
    """
    message = f"The '{deprecated_func}' function is deprecated"
    if deprecated_version:
        message += f" since {deprecated_version}"
    if not removal_version:
        removal_version = "a future release"
    message += f" and will be removed in {removal_version}."
    if replacing_func:
        message += f" Please use '{replacing_func}' instead."
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def safe_print(text: str):
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
