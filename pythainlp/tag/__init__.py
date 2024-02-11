# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Linguistic and other taggers.

Tagging each token in a sentence with supplementary information,
such as its part-of-speech (POS) tag, and named entity (NE) tag.
"""

__all__ = [
    "PerceptronTagger",
    "NER",
    "NNER",
    "chunk_parse",
    "pos_tag",
    "pos_tag_sents",
    "pos_tag_transformers",
    "tag_provinces",
]

from pythainlp.tag._tag_perceptron import PerceptronTagger
from pythainlp.tag.chunk import chunk_parse
from pythainlp.tag.locations import tag_provinces
from pythainlp.tag.named_entity import NER, NNER
from pythainlp.tag.pos_tag import pos_tag, pos_tag_sents, pos_tag_transformers
