# -*- coding: utf-8 -*-
from collections import Counter

from pythainlp.corpus import stopwords


# เรียงจำนวนคำของประโยค
def rank(data, stopword=False):
    """เรียงจำนวนคำของประโยค
    รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [ข้อความ,จำนวน]"""
    if stopword:
        data = [word for word in data if word not in stopwords.words("thai")]
        rankdata = Counter(data)
    else:
        rankdata = Counter(data)

    return rankdata


if __name__ == "__main__":
    text = [
        "แมว",
        "ชอบ",
        "ปลา",
        "แมว",
        "ชอบ",
        "นอน",
        "คน",
        "กลาย",
        "เป็น",
        "ทาส",
        "แมว",
    ]
    print(rank(text))
