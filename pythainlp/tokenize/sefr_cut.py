# -*- coding: utf-8 -*-
"""
Wrapper for SEFR CUT Thai word segmentation. SEFR CUT is a
Thai Word Segmentation Models using Stacked Ensemble.

:See Also:
    * `GitHub repository <https://github.com/mrpeerat/SEFR_CUT>`_
"""
from typing import List

import sefr_cut

_engine = 'ws1000'
sefr_cut.load_model(engine=_engine)


def segment(text: str, engine: str = 'ws1000') -> List[str]:
    """
    
    """
    global _engine
    if engine != _engine:
        _engine = engine
        sefr_cut.load_model(engine=_engine)
    return sefr_cut.tokenize(text)[0]