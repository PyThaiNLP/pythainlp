# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Cython-optimized text normalization functions.

Provides faster implementations of remove_tonemark and remove_dup_spaces
using C-level typed memory views and byte filtering.

These functions are API-compatible with their equivalents in
pythainlp.util.normalize and are loaded as transparent replacements when the
Cython extension is available.
"""
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import re as _re

from pythainlp import thai_tonemarks as _tonemarks_str

# Frozenset of tone mark characters for O(1) membership test.
# Must contain single-char strings (not ints): when Cython converts a
# Py_UCS4 value via the `in` operator it produces chr(c), not an integer.
cdef frozenset _TONE_SET = frozenset(_tonemarks_str)

# Use the same regex pattern as normalize.py to keep newline behaviour
# identical (collapses sequences of spaces+newlines into a single newline)
_RE_REMOVE_NEWLINES = _re.compile(r"[ \n]*\n[ \n]*")


cpdef str remove_tonemark(str text):
    """Remove Thai tone marks from text using UTF-8 byte-level filtering.

    Thai tone marks occupy the Unicode range U+0E48-U+0E4B, which encodes
    in UTF-8 as the three-byte sequence 0xE0 0xB9 {0x88-0x8B}.  Filtering
    at the byte level using typed memory views avoids per-character Python
    object creation and outperforms repeated str.replace() calls on long texts.

    :param text: input text
    :type text: str
    :return: text with all Thai tone marks removed
    :rtype: str
    """
    if not text:
        return text

    # Fast path: bail out early if none of the four tone marks are present
    cdef Py_UCS4 c
    cdef bint found = False
    for c in text:
        if c in _TONE_SET:
            found = True
            break
    if not found:
        return text

    # Encode once to UTF-8 bytes; use memoryview for C-level access.
    # IMPORTANT: the byte pattern below is hard-coded for the four Thai tone
    # marks U+0E48–U+0E4B (encoding: 0xE0 0xB9 {0x88–0x8B}).  If
    # pythainlp.thai_tonemarks is ever extended beyond those four codepoints
    # this filter will silently miss any additions; update the scan range
    # in the while-loop accordingly.
    cdef bytes src_bytes = text.encode("utf-8")
    cdef const unsigned char[:] src = src_bytes
    cdef Py_ssize_t n = len(src)

    # Pre-allocate output buffer (same size as input; result is always smaller)
    cdef bytearray dst_arr = bytearray(n)
    cdef unsigned char[:] dst = dst_arr
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t j = 0
    cdef unsigned char b0

    while i < n:
        b0 = src[i]
        # All Thai tone marks share first two bytes 0xE0 0xB9
        if b0 == 0xE0 and i + 2 < n and src[i + 1] == 0xB9:
            if 0x88 <= src[i + 2] <= 0x8B:
                i += 3  # skip tone-mark sequence
                continue
        dst[j] = b0
        j += 1
        i += 1

    return bytes(dst_arr[:j]).decode("utf-8")


cpdef str remove_dup_spaces(str text):
    """Remove duplicate ASCII spaces and collapse newlines; strip result.

    Behaviorally identical to pythainlp.util.normalize.remove_dup_spaces:
    - Only ASCII space (0x20) runs are collapsed (not tabs or other whitespace)
    - Newline normalisation is delegated to the same compiled regex

    :param text: input text
    :type text: str
    :return: text without duplicate spaces, with newlines normalised and
             leading/trailing whitespace stripped
    :rtype: str
    """
    cdef list out = []
    cdef Py_UCS4 c
    cdef bint prev_space = False
    for c in text:
        if c == 32:  # ASCII space 0x20
            if not prev_space:
                out.append(" ")
            prev_space = True
        else:
            out.append(chr(c))
            prev_space = False
    result = "".join(out)
    result = _RE_REMOVE_NEWLINES.sub("\n", result)
    return result.strip()
