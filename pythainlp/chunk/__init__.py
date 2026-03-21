# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai phrase structure (chunking) module.

This module provides chunk parsing for Thai text, following the
NLTK :mod:`nltk.chunk` naming convention.

:Example:

    .. code-block:: python

        from pythainlp.chunk import chunk_parse, CRFChunkParser
        from pythainlp.tag import pos_tag

        tokens = ["ผม", "รัก", "คุณ"]
        tokens_pos = pos_tag(tokens, engine="perceptron", corpus="orchid")

        # Using the convenience function
        print(chunk_parse(tokens_pos))
        # output: ['B-NP', 'B-VP', 'I-VP']

        # Using the class directly
        with CRFChunkParser() as parser:
            print(parser.parse(tokens_pos))
        # output: ['B-NP', 'B-VP', 'I-VP']
"""

from __future__ import annotations

__all__: list[str] = [
    "CRFChunkParser",
    "chunk_parse",
]

from pythainlp.chunk.crfchunk import CRFChunkParser


def chunk_parse(
    sent: list[tuple[str, str]],
    engine: str = "crf",
    corpus: str = "orchidpp",
) -> list[str]:
    """Parse a Thai sentence into phrase-structure chunks (IOB format).

    :param list[tuple[str, str]] sent: list of (word, POS-tag) pairs.
    :param str engine: chunking engine; currently only ``"crf"`` is
        supported.
    :param str corpus: corpus name for the CRF model; currently only
        ``"orchidpp"`` is supported.
    :return: list of IOB chunk labels, one per token.
    :rtype: list[str]

    :Example:

    .. code-block:: python

        from pythainlp.chunk import chunk_parse
        from pythainlp.tag import pos_tag

        tokens = ["ผม", "รัก", "คุณ"]
        tokens_pos = pos_tag(tokens, engine="perceptron", corpus="orchid")

        print(chunk_parse(tokens_pos))
        # output: ['B-NP', 'B-VP', 'I-VP']
    """
    _parser = CRFChunkParser(corpus=corpus)
    return _parser.parse(sent)
