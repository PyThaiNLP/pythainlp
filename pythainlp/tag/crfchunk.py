# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :mod:`pythainlp.chunk` instead.

.. deprecated:: 5.3.2
    This module has been superseded by :mod:`pythainlp.chunk`.
    Import :class:`pythainlp.chunk.CRFChunkParser` directly.
"""

from __future__ import annotations

from pythainlp.chunk.crfchunk import CRFChunkParser
from pythainlp.tools import warn_deprecation


# Backward-compatible alias. Deprecated since 5.3.2; removed in 6.0.
class CRFchunk(CRFChunkParser):
    """Deprecated. Use :class:`pythainlp.chunk.CRFChunkParser` instead.

    .. deprecated:: 5.3.2
        Use :class:`pythainlp.chunk.CRFChunkParser` instead.
    """

    def __init__(self, corpus: str = "orchidpp") -> None:
        warn_deprecation(
            "pythainlp.tag.crfchunk.CRFchunk",
            "pythainlp.chunk.CRFChunkParser",
            "5.3.2",
            "6.0",
        )
        super().__init__(corpus)
