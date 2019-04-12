# -*- coding: utf-8 -*-
"""
Thai Textbook Corpus (TTC) word frequency

Credit: Korakot Chaovavanich‎
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""

from pythainlp.corpus import get_corpus

__all__ = ["word_freqs"]

_FILENAME = "ttc_freq.txt"


def word_freqs():
    """
    Get word frequency from Thai Textbook Corpus (TTC)
    """
    lines = list(get_corpus(_FILENAME))
    listword = []
    for line in lines:
        listindata = line.split("\t")
        listword.append((listindata[0], int(listindata[1])))

    return listword
