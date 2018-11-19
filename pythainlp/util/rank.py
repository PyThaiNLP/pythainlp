# -*- coding: utf-8 -*-
from collections import Counter
from typing import List

from pythainlp.corpus import thai_stopwords

_STOPWORDS = thai_stopwords()


# เรียงจำนวนคำของประโยค
def rank(words: List[str], exclude_stopword: bool = False) -> Counter:
    """
    Sort words by frequency
    รับค่าเป็น ''list'' คืนค่าเป็น ''Counter'' Counter({"คำ": จำนวน, "คำ": จำนวน})
    """
    if not words:
        return None

    if exclude_stopword:
        words = [word for word in words if word not in _STOPWORDS]

    return Counter(words)
