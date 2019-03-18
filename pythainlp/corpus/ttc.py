# -*- coding: utf-8 -*-
"""
Thai Textbook Corpus (TTC) word frequency

Credit: Korakot Chaovavanich‎
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""
import os

from pythainlp.corpus import download as download_data
from pythainlp.tools import get_full_data_path

__all__ = ["word_freqs"]

def word_freqs():
    """
    Get word frequency from Thai Textbook Corpus (TTC)
    """
    path = get_full_data_path("ttc_freq.txt")  # try local copy first
    if not os.path.exists(path):  # if fail, download from internet
        download_data("ttc")

    with open(path, "r", encoding="utf8") as f:
        lines = f.read().splitlines()
    f.close()

    listword = []
    for line in lines:
        listindata = line.split("	")
        listword.append((listindata[0], int(listindata[1])))

    return listword
