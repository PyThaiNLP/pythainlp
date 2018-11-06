# -*- coding: utf-8 -*-
from collections import Counter

from pythainlp.corpus import thai_stopwords

_STOPWORDS = thai_stopwords()


# เรียงจำนวนคำของประโยค
def rank(words, stopword=False):
    """
    Sort words by frequency
    รับค่าเป็น ''list'' คืนค่าเป็น ''Counter'' Counter({"คำ": จำนวน, "คำ": จำนวน})
    """
    if not words:
        return None

    if stopword:
        words = [word for word in words if word not in _STOPWORDS]

    rankdata = Counter(words)

    return rankdata


if __name__ == "__main__":
    print(rank(["แมว", "ชอบ", "ปลา", "แมว", "ชอบ", "นอน", "คน", "เป็น", "ทาส", "แมว"]))
