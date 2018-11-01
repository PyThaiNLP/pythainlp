# -*- coding: utf-8 -*-
from collections import Counter

from pythainlp.corpus import thai_stopwords

_STOPWORDS = thai_stopwords()

# เรียงจำนวนคำของประโยค
def rank(data, stopword=False):
    """
    Sort words by frequency
    รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [(คำ, จำนวน), (คำ, จำนวน), ...]
    """
    if stopword:
        data = [word for word in data if word not in _STOPWORDS]

    rankdata = Counter(data)

    return rankdata


if __name__ == "__main__":
    text = ["แมว", "ชอบ", "ปลา", "แมว", "ชอบ", "นอน", "คน", "เป็น", "ทาส", "แมว"]
    print(rank(text))
