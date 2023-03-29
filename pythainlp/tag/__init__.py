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
Linguistic and other taggers.

Tagging each token in a sentence with supplementary information,
such as its part-of-speech (POS) tag, and named entity (NE) tag.
"""

__all__ = [
    "PerceptronTagger",
    "pos_tag",
    "pos_tag_sents",
    "tag_provinces",
    "chunk_parse",
    "NER",
    "NNER",
]

from pythainlp.tag.locations import tag_provinces
from pythainlp.tag.pos_tag import pos_tag, pos_tag_sents
from pythainlp.tag._tag_perceptron import PerceptronTagger
from pythainlp.tag.chunk import chunk_parse
from pythainlp.tag.named_entity import NER, NNER
