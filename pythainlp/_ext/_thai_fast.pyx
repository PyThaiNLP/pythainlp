# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Cython-optimized Thai character classification functions.

Provides faster implementations of is_thai_char, is_thai, and count_thai
by eliminating Python dispatch overhead and using C-level type declarations
for the inner character iteration loops.

These functions are API-compatible with their equivalents in
pythainlp.util.thai and are loaded as transparent replacements when the
Cython extension is available.
"""
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import string as _string

cdef unsigned int _TH_FIRST = 0x0E00  # U+0E00: first Thai character
cdef unsigned int _TH_LAST  = 0x0E7F  # U+0E7F: last Thai character


cpdef bint is_thai_char(object ch):
    """Return True if ch is a single Thai Unicode character.

    :param ch: input character (str or str-like object; must be exactly one character)
    :type ch: str
    :return: True if ch is a Thai character, otherwise False.
    :rtype: bool

    .. note::
        Unlike the pure-Python implementation (which raises ``TypeError``
        for empty or multi-character strings via ``ord()``), this
        implementation returns ``False`` for any input whose length is
        not exactly 1.
    """
    cdef str _ch = str(ch)
    if len(_ch) != 1:
        return False
    cdef Py_UCS4 c = _ch[0]
    return _TH_FIRST <= c <= _TH_LAST


cpdef bint is_thai(object text, object ignore_chars="."):
    """Return True if every non-ignored character in text is Thai.

    :param text: input text (str or str-like object)
    :type text: str
    :param ignore_chars: characters to ignore during validation;
        ``None`` is treated the same as ``""`` (no characters ignored)
    :type ignore_chars: str or None
    :return: True if text consists only of Thai and ignored characters
    :rtype: bool
    """
    cdef str _text = str(text)
    # Mirror the Python version: treat None/empty as "ignore nothing"
    if not ignore_chars:
        ignore_chars = ""
    cdef str _ic = ignore_chars
    cdef Py_UCS4 c
    for c in _text:
        if c not in _ic and not (_TH_FIRST <= c <= _TH_LAST):
            return False
    return True


# Match the default ignore_chars used by the Python count_thai implementation
_DEFAULT_IGNORE_CHARS: str = (
    _string.whitespace + _string.digits + _string.punctuation
)


cpdef double count_thai(object text, str ignore_chars=_DEFAULT_IGNORE_CHARS):
    """Return proportion of Thai characters in text (0.0–100.0).

    :param text: input text (str or str-like object); non-str values (including None) return 0.0
        to match the behaviour of the pure-Python implementation
    :type text: str
    :param ignore_chars: characters to exclude from the denominator,
        defaults to whitespace, digits, and punctuation marks
    :type ignore_chars: str
    :return: percentage of Thai characters in the non-ignored portion
    :rtype: float
    """
    # Matches Python version: non-str or falsy input → 0.0
    if not text or not isinstance(text, str):
        return 0.0
    cdef str _text = text
    # Normalise: treat empty string as no ignore chars (matches Python version)
    if not ignore_chars:
        ignore_chars = ""
    cdef Py_UCS4 c
    cdef Py_ssize_t num_thai = 0
    cdef Py_ssize_t num_ignore = 0
    cdef Py_ssize_t total = len(_text)
    for c in _text:
        if c in ignore_chars:
            num_ignore += 1
        elif _TH_FIRST <= c <= _TH_LAST:
            num_thai += 1
    cdef Py_ssize_t denom = total - num_ignore
    if denom == 0:
        return 0.0
    return (num_thai / denom) * 100.0
