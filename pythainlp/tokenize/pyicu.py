# -*- coding: utf-8 -*-
"""
Wrapper for PyICU word segmentation
https://github.com/ovalhub/pyicu
"""
import re
from typing import List

from icu import BreakIterator, Locale


def _gen_words(text: str) -> str:
    bd = BreakIterator.createWordInstance(Locale("th"))
    bd.setText(text)
    p = bd.first()
    for q in bd:
        yield text[p:q]
        p = q


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    text = re.sub("([^\u0E00-\u0E7F\n ]+)", " \\1 ", text)

    return list(_gen_words(text))
