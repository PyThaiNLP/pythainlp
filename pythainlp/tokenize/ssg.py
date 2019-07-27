# -*- coding: utf-8 -*-
from typing import List
import ssg
def segment(text: str) -> List[str]:
    return ssg.syllable_tokenize(text)