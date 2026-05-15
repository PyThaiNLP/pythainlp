# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Optional Cython-compiled extensions for performance-critical functions.

These extensions are built at install time when a C compiler and Cython are
available. If unavailable (e.g., PyPy, no compiler), the pure Python
implementations in pythainlp.util are used as fallback.
"""
