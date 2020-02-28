# -*- coding: utf-8 -*-
from typing import List

from ssg import syllable_tokenize


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    return syllable_tokenize(text)
