# -*- coding: utf-8 -*-
from typing import List

import ssg


def segment(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    return ssg.syllable_tokenize(text)
