# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple


def chunk_parse(
    sent: List[Tuple[str, str]],
    engine="crf", corpus="orchidpp"
) -> List[str]:
    """
    This function parse thai sentence to phrase structure in IOB format.

    :param list sent: list [(word,part-of-speech)]
    :param str engine: chunk parse engine (now, it has orchidpp only)

    :return: a list of tuple (word,part-of-speech,chunking)
    :rtype: List[str]
    """
    from .crfchunk import CRFchunk
    _engine = CRFchunk()
    return _engine.parse(sent)
