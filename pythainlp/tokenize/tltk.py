# -*- coding: utf-8 -*-
from typing import List
from tltk.nlp import word_segment as tltk_segment
from tltk.nlp import syl_segment


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []
    _temp = tltk_segment(text).replace("<u/>", "").replace("<s/>", " ")
    return _temp.split('|')


def syllable_tokenize(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []
    _temp = syl_segment(text)
    return _temp.split('~')
