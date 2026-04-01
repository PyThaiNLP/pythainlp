# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai soundex

Has multiple systems to choose from: Udom83 (default), LK82, MetaSound,
Complete Soundex, and Prayut & Somchaip
"""

from __future__ import annotations

from pythainlp.soundex import DEFAULT_SOUNDEX_ENGINE
from pythainlp.soundex.complete_soundex import complete_soundex
from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip
from pythainlp.soundex.udom83 import udom83

# Other Thai soundex systems (not implemented yet): Arun91, KSS97
# [KSS97] https://linux.thai.net/~thep/soundex/soundex.html


def soundex(
    text: str, engine: str = DEFAULT_SOUNDEX_ENGINE, length: int = 4
) -> str:
    """Converts Thai text into phonetic code.

    :param str text: word
    :param str engine: soundex engine
    :param int length: preferred length of the Soundex code (default is 4)\
        for metasound and prayut_and_somchaip only
    :return: Soundex code
    :rtype: str

    :Options for engine:
        * *udom83* (default) - Thai soundex algorithm proposed
          by Vichit Lorchirachoonkul [#udom83]_
        * *lk82* - Thai soundex algorithm proposed by
          Wannee Udompanich [#lk82]_
        * *metasound* - Thai soundex algorithm based on a combination
          of Metaphone and Soundex proposed by Snae & Brückner [#metasound]_
        * *prayut_and_somchaip* - Thai-English Cross-Language Transliterated
          Word Retrieval using Soundex Technique [#prayut_and_somchaip]_
        * *complete_soundex* - Complete Soundex for Thai Words Similarity
          Analysis [#complete_soundex]_

    :Example:

        >>> from pythainlp.soundex import soundex
        >>> soundex("ลัก")
        'ร100000'
        >>> soundex("ลัก", engine='lk82')
        'ร1000'
        >>> soundex("ลัก", engine='metasound')
        'ล100'
        >>> soundex("รัก")
        'ร100000'
        >>> soundex("รัก", engine='lk82')
        'ร1000'
        >>> soundex("รัก", engine='metasound')
        'ร100'
        >>> soundex("รักษ์")
        'ร100000'
        >>> soundex("รักษ์", engine='lk82')
        'ร1000'
        >>> soundex("รักษ์", engine='metasound')
        'ร100'
        >>> soundex("บูรณการ")
        'บ931900'
        >>> soundex("บูรณการ", engine='lk82')
        'บE419'
        >>> soundex("บูรณการ", engine='metasound')
        'บ551'
        >>> soundex("ปัจจุบัน")
        'ป775300'
        >>> soundex("ปัจจุบัน", engine='lk82')
        'ป3E54'
        >>> soundex("ปัจจุบัน", engine='metasound')
        'ป223'
        >>> soundex("vp", engine="prayut_and_somchaip")
        '11'
        >>> soundex("วีพี", engine="prayut_and_somchaip")
        '11'
        >>> soundex("ก้าน", engine="complete_soundex")
        'กก1Bน2-'
        >>> soundex("ทราย", engine="complete_soundex")
        'ซซ1Bย0-'
    """
    if engine == "lk82":
        _soundex = lk82(text)
    elif engine == "prayut_and_somchaip":
        _soundex = prayut_and_somchaip(text, length=length)
    elif engine == "metasound":
        _soundex = metasound(text, length=length)
    elif engine == "complete_soundex":
        _soundex = complete_soundex(text)
    else:  # default, use "udom83"
        _soundex = udom83(text)
    return _soundex
