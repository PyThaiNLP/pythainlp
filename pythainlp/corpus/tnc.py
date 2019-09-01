# -*- coding: utf-8 -*-
"""
Thai National Corpus word frequency

Credit: Korakot Chaovavanich‎
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""
import re
from typing import List, Tuple

import requests
from pythainlp.corpus import get_corpus

__all__ = ["word_freq", "word_freqs"]

_FILENAME = "tnc_freq.txt"


def word_freq(word: str, domain: str = "all") -> int:
    """

    .. note::
        **Not officially supported.**
        Get word frequency of a word by domain.
        This function will make a query to the server of
        Thai National Corpus.
        Internet connection is required.

    .. warning::
        Currently (as of 29 April 2019) it is likely to return 0,
        regardless of the word, as the service URL has been changed
        and the code is not updated yet.
        New URL is http://www.arts.chula.ac.th/~ling/tnc3/

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
    url = "http://www.arts.chula.ac.th/~ling/tnc3/"
    data = {"genre[]": "", "domain[]": listdomain[domain], "sortby": "perc", "p": word}

    r = requests.post(url, data=data)

    pat = re.compile(r'TOTAL</font>.*?#ffffff">(.*?)</font>', flags=re.DOTALL)
    match = pat.search(r.text)

    n = 0
    if match:
        n = int(match.group(1).strip())

    return n


def word_freqs() -> List[Tuple[str, int]]:
    """
    Get word frequency from Thai National Corpus (TNC)
    """
    lines = list(get_corpus(_FILENAME))
    word_freqs = []
    for line in lines:
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            word_freqs.append((word_freq[0], int(word_freq[1])))

    return word_freqs
