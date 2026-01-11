# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations


def chunk_parse(
    sent: list[tuple[str, str]], engine: str = "crf", corpus: str = "orchidpp"
) -> list[str]:
    """
    This function parses Thai sentence to phrase structure in IOB format.

    :param list sent: list [(word, part-of-speech)]
    :param str engine: chunk parse engine (now, it has crf only)
    :param str corpus: chunk parse corpus (now, it has orchidpp only)

    :return: a list of tuples (word, part-of-speech, chunking)
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.tag import chunk_parse, pos_tag

        tokens = ["ผม", "รัก", "คุณ"]
        tokens_pos = pos_tag(tokens, engine="perceptron", corpus="orchid")

        print(chunk_parse(tokens_pos))
        # output: ['B-NP', 'B-VP', 'I-VP']
    """
    from .crfchunk import CRFchunk

    _engine = CRFchunk()
    return _engine.parse(sent)
