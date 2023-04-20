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
from typing import List, Tuple


def chunk_parse(
    sent: List[Tuple[str, str]], engine: str = "crf", corpus: str = "orchidpp"
) -> List[str]:
    """
    This function parse thai sentence to phrase structure in IOB format.

    :param list sent: list [(word,part-of-speech)]
    :param str engine: chunk parse engine (now, it has crf only)
    :param str corpus: chunk parse corpus (now, it has orchidpp only)

    :return: a list of tuple (word,part-of-speech,chunking)
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.tag import chunk_parse, pos_tag

        tokens = ["ผม", "รัก", "คุณ"]
        tokens_pos = pos_tag(tokens, engine="perceptron", corpus="orchid")

        print(chunk_parse(tokens_pos))
        # output: ['B-NP', 'B-VP', 'I-VP']
    """
    from .crfchunk import CRFchunk

    _engine = CRFchunk()
    return _engine.parse(sent)
