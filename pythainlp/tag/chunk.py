# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple


def chunk_parse(
    sent: List[Tuple[str, str]],
    engine="crf", corpus="orchidpp"
    ) -> List[str]:
    from .crfchunk import CRFchunk
    _engine = CRFchunk()
    return _engine.parse(sent)
