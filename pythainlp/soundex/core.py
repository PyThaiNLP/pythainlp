# -*- coding: utf-8 -*-
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""
from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.udom83 import udom83
from pythainlp.soundex import DEFAULT_SOUNDEX_ENGINE

# Other Thai soundex systems (not implemented yet): Arun91, KSS97
# [KSS97] https://linux.thai.net/~thep/soundex/soundex.html


def soundex(text: str, engine: str = DEFAULT_SOUNDEX_ENGINE) -> str:
    """
    This function converts Thai text into phonetic code.

    :param str text: word
    :param str engine: soundex engine
    :return: Soundex code
    :rtype: str

    :Options for engine:
        * *udom83* (default) - Thai soundex algorithm proposed
          by Vichit Lorchirachoonkul [#udom83]_
        * *lk82* - Thai soundex algorithm proposed by
          Wannee Udompanich [#lk82]_
        * *metasound* - Thai soundex algorithm based on a combination
          of Metaphone and Soundex proposed by Snae & Brückner [#metasound]_

    :Example:
    ::

        from pythainlp.soundex import soundex

        soundex("ลัก"), soundex("ลัก", engine='lk82'), \\
            soundex("ลัก", engine='metasound')
        # output: ('ร100000', 'ร1000', 'ล100')

        soundex("รัก"), soundex("รัก", engine='lk82'), \\
            soundex("รัก", engine='metasound')
        # output: ('ร100000', 'ร1000', 'ร100')

        soundex("รักษ์"), soundex("รักษ์", engine='lk82'), \\
            soundex("รักษ์", engine='metasound')
        # output: ('ร100000', 'ร1000', 'ร100')

        soundex("บูรณการ"), soundex("บูรณการ", engine='lk82'), \\
            soundex("บูรณการ", engine='metasound')
        # output: ('บ931900', 'บE419', 'บ551')

        soundex("ปัจจุบัน"), soundex("ปัจจุบัน", engine='lk82'), \\
            soundex("ปัจจุบัน", engine='metasound')
        # output: ('ป775300', 'ป3E54', 'ป223')
    """
    if engine == "lk82":
        _soundex = lk82
    elif engine == "metasound":
        _soundex = metasound
    else:  # default, use "udom83"
        _soundex = udom83

    return _soundex(text)
