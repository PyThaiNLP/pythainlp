# -*- coding: utf-8 -*-
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""
from pythainlp.soundex.lk82 import lk82 as lk82
from pythainlp.soundex.metasound import metasound as metasound
from pythainlp.soundex.udom83 import udom83 as udom83

# Other Thai soundex systems (not implemented yet): Arun91, KSS97
# [KSS97] https://linux.thai.net/~thep/soundex/soundex.html


def soundex(text: str, engine="udom83") -> str:
    """
    Thai Soundex

    :param string text: word
    :param str engine: soundex engine
    :Parameters for engine:
        * udom83 (default)
        * lk82
        * metasound
    :return: soundex code
    """
    if engine == "udom83":
        _soundex = udom83
    elif engine == "lk82":
        _soundex = lk82
    elif engine == "metasound":
        _soundex = metasound
    else:  # default, use "udom83"
        _soundex = udom83

    return _soundex(text)
