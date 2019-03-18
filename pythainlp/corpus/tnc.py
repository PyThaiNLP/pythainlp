# -*- coding: utf-8 -*-
"""
Thai National Corpus word frequency

Credit: Korakot Chaovavanich‎
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""
import os
import re

from pythainlp.corpus import download as download_data
from pythainlp.corpus import get_corpus
from pythainlp.tools import get_full_data_path
import requests
__all__ = ["word_freq", "word_freqs"]


def word_freq(word, domain="all"):
    """
    Get word frequency of a word.
    This function will make a query to the server of Thai National Corpus.
    Internet connection is required.

    :param string word: word
    :param string domain: domain
    """
    listdomain = {
        "all": "",
        "imaginative": "1",
        "natural-pure-science": "2",
        "applied-science": "3",
        "social-science": "4",
        "world-affairs-history": "5",
        "commerce-finance": "6",
        "arts": "7",
        "belief-thought": "8",
        "leisure": "9",
        "others": "0",
    }
    url = "http://www.arts.chula.ac.th/~ling/TNCII/corp.php"
    data = {"genre[]": "", "domain[]": listdomain[domain], "sortby": "perc", "p": word}

    r = requests.post(url, data=data)

    pat = re.compile(r'TOTAL</font>(?s).*?#ffffff">(.*?)</font>')
    match = pat.search(r.text)

    n = 0
    if match:
        n = int(match.group(1).strip())

    return n


def word_freqs():
    """
    Get word frequency from Thai National Corpus (TNC)
    """
    lines = list(get_corpus("tnc_freq.txt"))
    listword = []
    for line in lines:
        listindata = line.split("	")
        listword.append((listindata[0], int(listindata[1])))

    return listword
