# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""
from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.udom83 import udom83
from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip
from pythainlp.soundex import DEFAULT_SOUNDEX_ENGINE

# Other Thai soundex systems (not implemented yet): Arun91, KSS97
# [KSS97] https://linux.thai.net/~thep/soundex/soundex.html


def soundex(
    text: str, engine: str = DEFAULT_SOUNDEX_ENGINE, length: int = 4
) -> str:
    """
    This function converts Thai text into phonetic code.

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
          Word Retrieval using Soundex Technique  [#prayut_and_somchaip]_

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

        soundex("vp", engine="prayut_and_somchaip")
        # output: '11'
        soundex("วีพี", engine="prayut_and_somchaip")
        # output: '11'
    """
    if engine == "lk82":
        _soundex = lk82(text)
    elif engine == "prayut_and_somchaip":
        _soundex = prayut_and_somchaip(text, length=length)
    elif engine == "metasound":
        _soundex = metasound(text, length=length)
    else:  # default, use "udom83"
        _soundex = udom83(text)
    return _soundex
