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
Thai Textbook Corpus (TTC) word frequency

Credit: Korakot Chaovavanich
https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
"""

__all__ = ["word_freqs", "unigram_word_freqs"]

from collections import defaultdict
from typing import List, Tuple

from pythainlp.corpus import get_corpus

_FILENAME = "ttc_freq.txt"


def word_freqs() -> List[Tuple[str, int]]:
    """
    Get word frequency from Thai Textbook Corpus (TTC)
    \n(See: `dev/pythainlp/corpus/ttc_freq.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/ttc_freq.txt>`_)
    """
    lines = list(get_corpus(_FILENAME))
    word_freqs = []
    for line in lines:
        word_freq = line.split("\t")
        if len(word_freq) >= 2:
            word_freqs.append((word_freq[0], int(word_freq[1])))

    return word_freqs


def unigram_word_freqs() -> defaultdict:
    """
    Get unigram word frequency from Thai Textbook Corpus (TTC)
    """
    lines = list(get_corpus(_FILENAME))
    _word_freqs = defaultdict(int)
    for i in lines:
        _temp = i.strip().split("	")
        if len(_temp) >= 2:
            _word_freqs[_temp[0]] = int(_temp[-1])

    return _word_freqs
