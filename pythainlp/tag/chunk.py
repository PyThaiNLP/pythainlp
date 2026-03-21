# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Deprecated. Use :func:`pythainlp.chunk.chunk_parse` instead.

.. deprecated:: 5.3.2
    :func:`chunk_parse` has moved to :mod:`pythainlp.chunk`.
"""

from __future__ import annotations

from pythainlp.chunk import chunk_parse as _chunk_parse
from pythainlp.tools import warn_deprecation


def chunk_parse(
    sent: list[tuple[str, str]],
    engine: str = "crf",
    corpus: str = "orchidpp",
) -> list[str]:
    """Parse a Thai sentence into phrase-structure chunks (IOB format).

    .. deprecated:: 5.3.2
        Use :func:`pythainlp.chunk.chunk_parse` instead.

    :param list[tuple[str, str]] sent: list of (word, POS-tag) pairs.
    :param str engine: chunking engine (default: ``"crf"``).
    :param str corpus: corpus name (default: ``"orchidpp"``).
    :return: list of IOB chunk labels, one per token.
    :rtype: list[str]
    """
    warn_deprecation(
        "pythainlp.tag.chunk_parse",
        "pythainlp.chunk.chunk_parse",
        "5.3.2",
        "6.0",
    )
    return _chunk_parse(sent, engine=engine, corpus=corpus)
