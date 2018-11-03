# -*- coding: utf-8 -*-
"""
Thai Textbook Corpus (TTC) word frequency

Credit: Korakot Chaovavanich‎
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""
import os

import requests
from pythainlp.tools import get_full_data_path

__all__ = ["get_word_frequency_all"]

_TCC_FREQ_URL = "https://raw.githubusercontent.com/korakot/thainlp/master/ttc_freq.txt"


def get_word_frequency_all():
    """
    ดึงข้อมูลความถี่คำของ Thai Textbook Corpus (TTC) มาใช้งาน
    โดยมีรูปแบบข้อมูลเป็น List[Tuple] [(word, frequency), ...]
    """
    path = get_full_data_path("tnc_freq.txt")  # try local copy first
    if not os.path.exists(path):  # if fail, download from internet
        response = requests.get(_TCC_FREQ_URL)
        with open(path, "wb") as f:
            f.write(response.content)
        f.close()

    with open(path, "r", encoding="utf8") as f:
        lines = f.read().splitlines()
    f.close()

    listword = []
    for line in lines:
        listindata = line.split("	")
        listword.append((listindata[0], int(listindata[1])))

    return listword
